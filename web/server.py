"""
FastAPI server — Academic Debate Arena
Run: uvicorn web.server:app --reload --port 8000
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import asyncio
import json
import queue
import threading
from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
from orchestrator import create_session, generate_opening_question
from agents.professor import generate_professor_turn
from agents.moderator import generate_moderator_summary, generate_final_summary
from agents.fact_checker import fact_check_turn
from agents.research_synthesizer import generate_research_kit, save_research_kit
from output.exporter import export_markdown
from debate.session import Turn

app = FastAPI(title="Academic Debate Arena")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React build (sau khi build xong)
static_dir = os.path.join(os.path.dirname(__file__), "dist")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")


# ── Models ────────────────────────────────────────────────────────────────────

class DebateRequest(BaseModel):
    topic: str
    field: str


# ── SSE helper ────────────────────────────────────────────────────────────────

def _sse(event: str, data: dict) -> str:
    """Format an SSE message."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


# ── Debate runner (runs in a separate thread, pushes events to queue) ─────────

def _run_debate(topic: str, field: str, q: queue.Queue):
    """Run the full debate and push events into the queue."""
    try:
        print(f"[Debate] Starting: {topic}", flush=True)
        
        # 1. Create professors
        q.put(_sse("status", {"message": "Creating professor profiles..."}))
        print("[Debate] Creating session...", flush=True)
        session = create_session(topic, field)
        print(f"[Debate] Session created with {len(session.professors)} professors", flush=True)

        profs_data = [
            {"key": p.key, "name": p.name, "university": p.university,
             "role": p.role, "stance": p.stance, "expertise": p.expertise}
            for p in session.professors
        ]
        q.put(_sse("professors", {"professors": profs_data}))
        print(f"[Debate] Sent professors data", flush=True)

        # 2. Opening
        q.put(_sse("status", {"message": "Moderator is preparing..."}))
        print("[Debate] Generating opening question...", flush=True)
        opening = generate_opening_question(topic, session.professors)
        turn = Turn(turn_number=session.current_turn, speaker_key="moderator",
                    speaker_name="Moderator", role="Moderator",
                    content=opening, is_moderator=True)
        session.add_turn(turn)
        q.put(_sse("moderator", {"turn": session.current_turn - 1,
                                  "label": "Opening", "content": opening}))
        print("[Debate] Opening sent", flush=True)

        # 3. Debate loop
        for round_num in range(1, config.MAX_ROUNDS + 1):
            session.current_round = round_num
            print(f"[Debate] Round {round_num}", flush=True)
            q.put(_sse("round", {"round": round_num}))

            for _ in range(config.MAX_TURNS_PER_ROUND):
                for prof in session.professors:
                    turn_num = session.current_turn
                    print(f"[Debate] {prof.name} speaking (turn {turn_num})", flush=True)

                    # Notify who is speaking next
                    q.put(_sse("speaker_start", {
                        "turn": turn_num,
                        "key": prof.key,
                        "name": prof.name,
                        "role": prof.role,
                    }))

                    # Stream chunks
                    chunks = []
                    def on_chunk(text, _q=q, _chunks=chunks):
                        _chunks.append(text)
                        _q.put(_sse("chunk", {"text": text}))

                    try:
                        generate_professor_turn(prof, session, stream_callback=on_chunk)
                    except Exception as e:
                        print(f"[Debate ERROR] Failed to generate turn for {prof.name}: {e}", flush=True)
                        raise
                    
                    full_text = "".join(chunks)
                    print(f"[Debate] {prof.name} generated {len(full_text)} chars", flush=True)

                    # Fact-check
                    q.put(_sse("status", {"message": f"Fact-checking {prof.name}..."}))
                    try:
                        fact_tags = fact_check_turn(full_text, prof.name)
                    except Exception as e:
                        print(f"[Debate WARNING] Fact check failed for {prof.name}: {e}", flush=True)
                        fact_tags = []

                    # Save turn
                    turn = Turn(turn_number=turn_num, speaker_key=prof.key,
                                speaker_name=prof.name, role=prof.role,
                                content=full_text, fact_tags=fact_tags)
                    session.add_turn(turn)

                    # Send fact tags
                    q.put(_sse("speaker_end", {
                        "turn": turn_num,
                        "key": prof.key,
                        "fact_tags": fact_tags,
                    }))

            # Moderator summary
            if round_num < config.MAX_ROUNDS:
                q.put(_sse("status", {"message": f"Moderator is summarizing round {round_num}..."}))
                try:
                    summary = generate_moderator_summary(session)
                except Exception as e:
                    print(f"[Debate WARNING] Moderator summary failed: {e}", flush=True)
                    summary = "(Summary unavailable)"
                
                mod_turn = Turn(turn_number=session.current_turn, speaker_key="moderator",
                                speaker_name="Moderator", role="Moderator",
                                content=summary, is_moderator=True)
                session.add_turn(mod_turn)
                q.put(_sse("moderator", {
                    "turn": session.current_turn - 1,
                    "label": f"Round {round_num} Summary",
                    "content": summary,
                }))

        # 4. Final summary
        q.put(_sse("status", {"message": "Writing final summary..."}))
        try:
            final = generate_final_summary(session)
        except Exception as e:
            print(f"[Debate WARNING] Final summary failed: {e}", flush=True)
            final = "(Final summary unavailable)"
        
        q.put(_sse("final", {"content": final}))

        # 5. Save transcript
        if config.SAVE_TRANSCRIPT:
            try:
                filename = export_markdown(session, config.TRANSCRIPT_DIR)
                q.put(_sse("saved", {"filename": filename}))
                print(f"[Debate] Transcript saved: {filename}", flush=True)
            except Exception as e:
                print(f"[Debate WARNING] Failed to save transcript: {e}", flush=True)
        
        # 6. Generate research kit (if RESEARCH_MODE is ON)
        if config.RESEARCH_MODE:
            q.put(_sse("status", {"message": "Synthesizing research insights..."}))
            try:
                research_kit = generate_research_kit(session, session.topic, session.field)
                # Save research kit to files
                kit_filename = save_research_kit(research_kit, config.RESEARCH_KIT_DIR)
                
                # Send comprehensive research insights to UI
                q.put(_sse("research_kit", {
                    "outline": research_kit.get("outline", ""),
                    "key_findings": research_kit.get("key_findings", []),
                    "research_gaps": research_kit.get("research_gaps", []),  # NEW
                    "novel_approaches": research_kit.get("novel_approaches", []),  # NEW
                    "breakthrough_areas": research_kit.get("breakthrough_areas", []),  # NEW
                    "theoretical_foundations": research_kit.get("theoretical_foundations", []),  # NEW
                    "methodology_innovations": research_kit.get("methodology_innovations", []),  # NEW
                    "cross_domain_insights": research_kit.get("cross_domain_insights", []),  # NEW
                    "counterarguments": research_kit.get("counterarguments", {}),  # NEW
                    "mathematical_frameworks": research_kit.get("mathematical_frameworks", []),  # MATHEMATICAL ANALYSIS
                    "mathematical_gaps": research_kit.get("mathematical_gaps", {}),  # MATHEMATICAL ANALYSIS
                    "mathematical_comparison": research_kit.get("mathematical_comparison", []),  # MATHEMATICAL ANALYSIS
                    "foundational_papers": research_kit.get("foundational_papers", {}),  # ACADEMIC RIGOR
                    "verified_claims": research_kit.get("verified_claims", {}),  # ACADEMIC RIGOR
                    "citation_analysis": research_kit.get("citation_analysis", {}),  # ACADEMIC RIGOR
                    "debate_rigor": research_kit.get("debate_rigor", {}),  # ACADEMIC RIGOR
                    "evidence_strength": research_kit.get("evidence_strength", {}),  # EVIDENCE VALIDATION
                    "gap_foundation_solution": research_kit.get("gap_foundation_solution", {}),  # ARGUMENT STRUCTURE
                    "open_questions": research_kit.get("open_questions", []),
                    "recommendations": research_kit.get("recommendations", []),
                }))
                q.put(_sse("saved", {"filename": kit_filename}))
                print(f"[Debate] Research kit generated and saved: {kit_filename}", flush=True)
            except Exception as e:
                print(f"[Debate WARNING] Research kit generation failed: {e}", flush=True)
                import traceback
                traceback.print_exc()
        
        print("[Debate] Completed successfully", flush=True)

    except Exception as e:
        error_msg = str(e)
        print(f"[Debate FATAL ERROR] {error_msg}", flush=True)
        import traceback
        traceback.print_exc()
        q.put(_sse("error", {"message": error_msg}))
    finally:
        q.put(None)  # sentinel — stream finished


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def index():
    from fastapi.responses import FileResponse
    dist_index = os.path.join(os.path.dirname(__file__), "dist", "index.html")
    if os.path.exists(dist_index):
        return FileResponse(dist_index)
    return {"message": "Academic Debate Arena API", "docs": "/docs"}


@app.post("/api/debate/stream")
def debate_stream(req: DebateRequest):
    """SSE endpoint — stream the full debate session."""
    print(f"[API] /api/debate/stream called: {req.topic[:50]}", flush=True)
    q: queue.Queue = queue.Queue()

    # Run the debate in a separate thread to avoid blocking
    thread = threading.Thread(
        target=_run_debate,
        args=(req.topic, req.field, q),
        daemon=True,
    )
    thread.start()

    def generate() -> Generator:
        print("[API] SSE stream generator started", flush=True)
        try:
            while True:
                item = q.get()
                if item is None:
                    print("[API] SSE stream ending (sentinel received)", flush=True)
                    break
                yield item
        except Exception as e:
            print(f"[API] Error in generator: {e}", flush=True)
            raise

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "model": config.MODEL}


# ── Session History endpoints ──────────────────────────────────────────────────

@app.get("/api/history")
def list_history():
    """Return a list of saved transcripts."""
    transcript_dir = config.TRANSCRIPT_DIR
    if not os.path.exists(transcript_dir):
        return {"sessions": []}

    sessions = []
    for fname in sorted(os.listdir(transcript_dir), reverse=True):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(transcript_dir, fname)
        # Read a few header lines to get topic + field
        try:
            with open(fpath, encoding="utf-8") as f:
                lines = [f.readline().strip() for _ in range(4)]
            topic = lines[1].replace("**Topic:**", "").strip()
            field = lines[2].replace("**Field:**", "").strip()
            date  = lines[3].replace("**Date:**", "").strip()[:19].replace("T", " ")
            size  = os.path.getsize(fpath)
            sessions.append({
                "filename": fname,
                "topic": topic,
                "field": field,
                "date": date,
                "size": size,
            })
        except Exception:
            continue

    return {"sessions": sessions}


@app.get("/api/history/{filename}")
def get_transcript(filename: str):
    """Return markdown content of a transcript."""
    # Only allow reading `.md` files inside the transcripts directory
    if not filename.endswith(".md") or "/" in filename or "\\" in filename:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid filename")

    fpath = os.path.join(config.TRANSCRIPT_DIR, filename)
    if not os.path.exists(fpath):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")

    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    return {"filename": filename, "content": content}


# ── Session History ───────────────────────────────────────────────────────────

@app.get("/api/history")
def get_history():
    """Return a list of saved transcripts."""
    import glob
    from pathlib import Path

    transcript_dir = config.TRANSCRIPT_DIR
    if not os.path.exists(transcript_dir):
        return {"sessions": []}

    files = sorted(glob.glob(f"{transcript_dir}/*.md"), reverse=True)
    sessions = []
    for f in files[:20]:  # at most 20 recent sessions
        path = Path(f)
        # Read the first few lines to get topic/field
        lines = path.read_text(encoding="utf-8").splitlines()
        topic, field, date = "", "", ""
        for line in lines[:6]:
            if line.startswith("**Topic:**"):
                topic = line.replace("**Topic:**", "").strip()
            elif line.startswith("**Field:**"):
                field = line.replace("**Field:**", "").strip()
            elif line.startswith("**Date:**"):
                date = line.replace("**Date:**", "").strip()[:19]
        sessions.append({
            "filename": path.name,
            "topic": topic,
            "field": field,
            "date": date,
        })
    return {"sessions": sessions}


@app.get("/api/history/{filename}")
def get_transcript(filename: str):
    """Return the content of a specific transcript."""
    from pathlib import Path
    # Sanitize filename — allow `.md` only, prevent path traversal
    if "/" in filename or "\\" in filename or not filename.endswith(".md"):
        return {"error": "Invalid filename"}
    path = Path(config.TRANSCRIPT_DIR) / filename
    if not path.exists():
        return {"error": "Not found"}
    return {"content": path.read_text(encoding="utf-8")}
