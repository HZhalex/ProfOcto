"""
FastAPI server — Academic Debate Arena
Chạy: uvicorn web.server:app --reload --port 8000
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
    """Format một SSE message."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


# ── Debate runner (chạy trong thread riêng, đẩy events vào queue) ─────────────

def _run_debate(topic: str, field: str, q: queue.Queue):
    """Toàn bộ logic debate chạy ở đây, gửi events vào queue."""
    try:
        # 1. Tạo professors
        q.put(_sse("status", {"message": "Đang tạo professor profiles..."}))
        session = create_session(topic, field)

        profs_data = [
            {"key": p.key, "name": p.name, "university": p.university,
             "role": p.role, "stance": p.stance, "expertise": p.expertise}
            for p in session.professors
        ]
        q.put(_sse("professors", {"professors": profs_data}))

        # 2. Opening
        q.put(_sse("status", {"message": "Moderator đang chuẩn bị..."}))
        opening = generate_opening_question(topic, session.professors)
        turn = Turn(turn_number=session.current_turn, speaker_key="moderator",
                    speaker_name="Moderator", role="Moderator",
                    content=opening, is_moderator=True)
        session.add_turn(turn)
        q.put(_sse("moderator", {"turn": session.current_turn - 1,
                                  "label": "Mở màn", "content": opening}))

        # 3. Debate loop
        for round_num in range(1, config.MAX_ROUNDS + 1):
            session.current_round = round_num
            q.put(_sse("round", {"round": round_num}))

            for _ in range(config.MAX_TURNS_PER_ROUND):
                for prof in session.professors:
                    turn_num = session.current_turn

                    # Thông báo ai sắp nói
                    q.put(_sse("speaker_start", {
                        "turn": turn_num,
                        "key": prof.key,
                        "name": prof.name,
                        "role": prof.role,
                    }))

                    # Stream từng chunk
                    chunks = []
                    def on_chunk(text, _q=q, _chunks=chunks):
                        _chunks.append(text)
                        _q.put(_sse("chunk", {"text": text}))

                    generate_professor_turn(prof, session, stream_callback=on_chunk)
                    full_text = "".join(chunks)

                    # Fact-check
                    q.put(_sse("status", {"message": f"Fact-checking {prof.name}..."}))
                    fact_tags = fact_check_turn(full_text, prof.name)

                    # Lưu turn
                    turn = Turn(turn_number=turn_num, speaker_key=prof.key,
                                speaker_name=prof.name, role=prof.role,
                                content=full_text, fact_tags=fact_tags)
                    session.add_turn(turn)

                    # Gửi fact tags
                    q.put(_sse("speaker_end", {
                        "turn": turn_num,
                        "key": prof.key,
                        "fact_tags": fact_tags,
                    }))

            # Moderator tóm tắt
            if round_num < config.MAX_ROUNDS:
                q.put(_sse("status", {"message": f"Moderator tóm tắt round {round_num}..."}))
                summary = generate_moderator_summary(session)
                mod_turn = Turn(turn_number=session.current_turn, speaker_key="moderator",
                                speaker_name="Moderator", role="Moderator",
                                content=summary, is_moderator=True)
                session.add_turn(mod_turn)
                q.put(_sse("moderator", {
                    "turn": session.current_turn - 1,
                    "label": f"Tóm tắt Round {round_num}",
                    "content": summary,
                }))

        # 4. Final summary
        q.put(_sse("status", {"message": "Đang tổng kết..."}))
        final = generate_final_summary(session)
        q.put(_sse("final", {"content": final}))

        # 5. Lưu transcript
        if config.SAVE_TRANSCRIPT:
            filename = session.save_transcript(config.TRANSCRIPT_DIR)
            q.put(_sse("saved", {"filename": filename}))

    except Exception as e:
        q.put(_sse("error", {"message": str(e)}))
    finally:
        q.put(None)  # sentinel — báo stream kết thúc


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
    """SSE endpoint — stream toàn bộ cuộc tranh luận."""
    q: queue.Queue = queue.Queue()

    # Chạy debate trong thread riêng để không block event loop
    thread = threading.Thread(
        target=_run_debate,
        args=(req.topic, req.field, q),
        daemon=True,
    )
    thread.start()

    def generate() -> Generator:
        while True:
            item = q.get()
            if item is None:
                break
            yield item

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