#!/usr/bin/env python3
"""
Academic Debate Arena
Chạy: python main.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from rich.prompt import Prompt

import config
from orchestrator import create_session, generate_opening_question
from agents.professor import generate_professor_turn
from agents.moderator import generate_moderator_summary, generate_final_summary
from agents.fact_checker import fact_check_turn
from agents.research_synthesizer import generate_research_kit, save_research_kit
from agents.theorem_extractor import extract_theorems, extract_citations
from agents.rigor_scorer import score_mathematical_rigor, compare_rigor
from agents.gap_identifier import identify_research_gaps, generate_phd_research_recommendations
from agents.gap_to_formal_problem import formalize_all_gaps
from agents.novelty_analyzer import analyze_novelty_batch, filter_iclr_promising
from agents.solution_sketch import generate_sketches_batch, rank_by_feasibility
from agents.iclr_readiness_scorer import assess_batch, format_executive_summary
from debate.session import Turn
from debate.turn_manager import TurnManager
from output.terminal_renderer import (
    console, print_header, print_professors_table, print_round_header,
    print_moderator_turn, print_professor_header, print_fact_tags,
    print_final_summary, print_saved, stream_write,
)
from output.exporter import export_markdown
from utils.logger import init_logger, get_logger


def run_debate(topic: str, field: str):

    # ── 0. Initialize Logging ─────────────────────────────────
    session_name = topic[:40].replace(" ", "_").replace("/", "-")
    logger = init_logger(session_name)
    logger.log_debate_start(topic, field, [])  # Empty list, will add professors later

    # ── 1. Setup ──────────────────────────────────────────────
    print_header(topic, field)
    console.print("[dim]Đang tạo professor profiles...[/dim]")
    session = create_session(topic, field)
    logger.log_debate_start(topic, field, session.professors)  # Update with actual professors
    print_professors_table(session.professors)

    # Khởi tạo TurnManager
    turn_mgr = TurnManager(session)

    # ── 2. Opening ────────────────────────────────────────────
    console.print("[dim]Moderator đang chuẩn bị...[/dim]\n")
    opening = generate_opening_question(topic, session.professors)
    turn = Turn(turn_number=session.current_turn, speaker_key="moderator",
                speaker_name="Moderator", role="Moderator",
                content=opening, is_moderator=True)
    session.add_turn(turn)
    print_moderator_turn(opening, turn.turn_number, "Moderator — Mở màn")

    # ── 3. Main debate loop ───────────────────────────────────
    for round_num in range(1, config.MAX_ROUNDS + 1):
        session.current_round = round_num
        print_round_header(round_num)

        for _ in range(config.MAX_TURNS_PER_ROUND):
            for _ in range(len(session.professors)):
                prof = turn_mgr.next_professor()
                turn_num = session.current_turn
                print_professor_header(prof, turn_num, session.professors)

                # Stream response
                if config.STREAM_OUTPUT:
                    console.print()
                    def make_callback():
                        buf = []
                        def cb(text):
                            buf.append(text)
                            stream_write(text)
                        def get(): return "".join(buf)
                        return cb, get
                    cb, get_text = make_callback()
                    generate_professor_turn(prof, session, stream_callback=cb)
                    full_text = get_text()
                    console.print("\n")
                else:
                    full_text = generate_professor_turn(prof, session)
                    console.print(full_text)
                    console.print()

                # Cảnh báo nếu đang lặp lại
                if turn_mgr.is_repeating(full_text, prof.key):
                    console.print(f"  [dim yellow]⚠ {prof.name} có xu hướng lặp lại ý[/dim yellow]")

                # Fact-check
                fact_tags = fact_check_turn(full_text, prof.name)
                if fact_tags:
                    print_fact_tags(fact_tags)
                    console.print()
                
                # NEW: Mathematical rigor analysis (PhD focus)
                theorems_data = {}
                citations = []
                rigor_score = {}
                
                if config.THEOREM_EXTRACTION_ENABLED:
                    theorems_data = extract_theorems(full_text, prof.name)
                    citations = extract_citations(full_text)
                    
                    if config.RIGOR_SCORING_ENABLED:
                        rigor_score = score_mathematical_rigor(full_text, prof.name)
                        session.add_rigor_score(prof.name, rigor_score)
                        
                        if config.SHOW_RIGOR_SCORES:
                            verdict_colors = {
                                "HIGHLY_RIGOROUS": "green",
                                "RIGOROUS": "cyan",
                                "MODERATELY_BACKED": "yellow",
                                "OPINION_BASED": "yellow",
                                "UNSUPPORTED": "red"
                            }
                            color = verdict_colors.get(rigor_score.get("verdict", ""), "white")
                            console.print(f"  [{color}]📊 Rigor Score: {rigor_score.get('rigor_score', 0)}/10 — {rigor_score.get('verdict', '')}")
                            if config.DETAILED_THEOREM_ANALYSIS and theorems_data.get("theorems"):
                                console.print(f"  [dim]  Theorems cited: {rigor_score.get('details', {}).get('num_theorems_cited', 0)}, Papers: {rigor_score.get('details', {}).get('num_papers_cited', 0)}, Proof density: {int(rigor_score.get('details', {}).get('proof_coverage', 0)*100)}%[/dim]")

                # Lưu turn với theorem & rigor data
                session.add_turn(Turn(
                    turn_number=turn_num, speaker_key=prof.key,
                    speaker_name=prof.name, role=prof.role,
                    content=full_text, fact_tags=fact_tags,
                    theorems_data=theorems_data,
                    rigor_score=rigor_score,
                    citations=citations,
                ))

        # Moderator tóm tắt
        if round_num < config.MAX_ROUNDS:
            console.print("[dim]Moderator đang tóm tắt...[/dim]")
            summary = generate_moderator_summary(session)
            mod_turn = Turn(turn_number=session.current_turn, speaker_key="moderator",
                            speaker_name="Moderator", role="Moderator",
                            content=summary, is_moderator=True)
            session.add_turn(mod_turn)
            print_moderator_turn(summary, mod_turn.turn_number,
                                 f"Moderator — Tóm tắt Round {round_num}")

    # ── 4. Stats từ TurnManager ───────────────────────────────
    stats = turn_mgr.get_stats()
    console.print("\n[dim]Turn stats: " +
                  " | ".join(f"{n}: {c}" for n, c in stats.items()) + "[/dim]")

    # ── 5. Final summary ──────────────────────────────────────
    console.print("[dim]Đang tổng kết...[/dim]\n")
    final = generate_final_summary(session)
    print_final_summary(final)
    
    # NEW: PhD Analysis - Research Gap Identification & Recommendations ──
    if config.RESEARCH_GAP_DETECTION_ENABLED:
        console.print("\n[dim]Phân tích research gaps dành cho PhD students...[/dim]\n")
        
        # Identify gaps
        all_turns_for_gap_analysis = []
        for turn in session.turns:
            if not turn.is_moderator:
                all_turns_for_gap_analysis.append({
                    "speaker": turn.speaker_name,
                    "theorems_data": turn.theorems_data if hasattr(turn, 'theorems_data') else {},
                    "content": turn.content
                })
        
        gaps = identify_research_gaps(all_turns_for_gap_analysis, session.topic)
        session.set_research_gaps(gaps)
        
        if gaps:
            console.print("[bold cyan]🔬 RESEARCH GAPS FOR PhD STUDENTS[/bold cyan]\n")
            for i, gap in enumerate(gaps[:5], 1):
                console.print(f"[bold]{i}. {gap.get('title', 'Unknown gap')}[/bold]")
                console.print(f"   Difficulty: {gap.get('difficulty', 'Unknown')}")
                console.print(f"   PhD Value: {gap.get('phd_value', 'Unknown')}")
                if gap.get('industry_impact'):
                    console.print(f"   Industry Impact: {gap['industry_impact']}")
                console.print()
        
        # Generate PhD recommendations
        if config.PhD_RECOMMENDATIONS_ENABLED:
            console.print("[dim]Sinh ra research recommendations...[/dim]\n")
            phd_recommendations = generate_phd_research_recommendations(gaps)
            session.set_phd_recommendations(phd_recommendations)
            if phd_recommendations:
                console.print(phd_recommendations)
    
    # NEW: Show rigor score comparison if multiple professors
    if config.SHOW_RIGOR_SCORES and len(session.professors) > 1:
        console.print("\n[bold cyan]📊 MATHEMATICAL RIGOR TALLY[/bold cyan]\n")
        prof_scores = {}
        for prof in session.professors:
            avg_score = session.get_average_rigor_score(prof.name)
            prof_scores[prof.name] = avg_score
            console.print(f"{prof.name}: {avg_score:.1f}/10")
        console.print()
    
    # NEW: ICLR READINESS PIPELINE (Phase 5) ──────────────────
    # Convert gaps → formal problems → novelty assessment → solution sketches → readiness scores
    if config.ICLR_READINESS_ENABLED and session.research_gaps:
        console.print("\n[bold bright_cyan]━━━ ICLR READINESS ASSESSMENT PIPELINE ━━━[/bold bright_cyan]\n")
        
        try:
            # Initialize variables for each phase (to avoid NameError if a phase is disabled)
            formal_problems = []
            novelty_results = []
            solution_sketches = []
            
            # Prepare debate context for tracing
            debate_context = {
                "turns": [{
                    "speaker": t.speaker_name,
                    "role": t.role,
                    "content": t.content
                } for t in session.turns if not t.is_moderator],
                "all_professors": [{
                    "name": p.name,
                    "role": p.role,
                    "stance": p.stance,
                    "expertise": p.expertise
                } for p in session.professors]
            }
            
            # Collect all citations from debate
            all_citations = []
            for turn in session.turns:
                if hasattr(turn, 'citations') and turn.citations:
                    for citation in turn.citations:
                        citation["cited_by_professor"] = turn.speaker_name
                        all_citations.append(citation)
            
            # Collect rigor scores
            all_rigor_scores = []
            for prof in session.professors:
                avg = session.get_average_rigor_score(prof.name)
                all_rigor_scores.append(avg)
            
            # Phase 5-1: Gap → Formal Problem
            if config.GAP_TO_FORMAL_PROBLEM_ENABLED and config.SHOW_FORMAL_PROBLEMS:
                console.print("[dim]→ Formalizing gaps to mathematical problems...[/dim]")
                formal_problems = formalize_all_gaps(session.research_gaps, debate_context, session.topic)
                session.set_formal_problems(formal_problems)
                console.print(f"[green]✓ Formalized {len(formal_problems)} problems[/green]\n")
            
            # Phase 5-2: Novelty Analysis
            if config.NOVELTY_ANALYZER_ENABLED and config.SHOW_NOVELTY_ANALYSIS:
                console.print("[dim]→ Analyzing novelty vs SOTA...[/dim]")
                novelty_results = analyze_novelty_batch(
                    formal_problems if formal_problems else [],
                    all_citations,
                    debate_context,
                    session.topic
                )
                session.set_novelty_assessments(novelty_results)
                console.print(f"[green]✓ Analyzed {len(novelty_results)} problems[/green]\n")
            
            # Phase 5-3: Solution Sketches
            if config.SOLUTION_SKETCH_ENABLED and config.SHOW_SOLUTION_SKETCHES:
                console.print("[dim]→ Generating solution sketches from debate arguments...[/dim]")
                
                # Collect professor arguments
                professor_arguments = []
                for turn in session.turns:
                    if not turn.is_moderator and hasattr(turn, 'theorems_data'):
                        professor_arguments.append({
                            "professor": turn.speaker_name,
                            "argument": turn.content[:100],
                            "mathematical_support": turn.theorems_data.get("summary", "")
                        })
                
                solution_sketches = generate_sketches_batch(
                    formal_problems if formal_problems else [],
                    debate_context,
                    professor_arguments
                )
                session.set_solution_sketches(solution_sketches)
                console.print(f"[green]✓ Generated {len(solution_sketches)} solution sketches[/green]\n")
            
            # Phase 5-4: ICLR Readiness Assessment
            if config.ICLR_READINESS_ENABLED and config.SHOW_ICLR_READINESS:
                console.print("[dim]→ Assessing ICLR readiness for PhD pursuit...[/dim]")
                readiness_scores = assess_batch(
                    formal_problems if formal_problems else [],
                    novelty_results if novelty_results else [],
                    solution_sketches if solution_sketches else [],
                    all_rigor_scores
                )
                session.set_iclr_readiness_scores(readiness_scores)
                console.print(f"[green]✓ Assessed readiness for {len(readiness_scores)} gaps[/green]\n")
                
                # Display executive summary
                if readiness_scores:
                    summary = format_executive_summary(readiness_scores, top_n=3)
                    console.print(summary)
                
                # Display action items for top gap if enabled
                if config.SHOW_ACTION_ITEMS and readiness_scores:
                    top_gap = readiness_scores[0]
                    if top_gap.get("action_items"):
                        console.print("[bold cyan]🎯 ACTION ITEMS (Top priority gap):[/bold cyan]\n")
                        for item in top_gap.get("action_items", [])[:5]:
                            priority_icon = "🔴" if item.get("priority") == "High" else "🟡" if item.get("priority") == "Medium" else "🟢"
                            console.print(f"{priority_icon} [{item.get('priority')}] {item.get('action')}")
                            console.print(f"    ⏱ {item.get('timeline')}\n")
        
        except Exception as e:
            logger.log_error("iclr_pipeline", e, context="Phase 5 ICLR pipeline error")
            console.print(f"[red]⚠ ICLR pipeline error: {str(e)}[/red]\n")
    
    # ── Log debate completion ─────────────────────────────────
    logger = get_logger()
    final_scores = {prof.name: session.get_average_rigor_score(prof.name) for prof in session.professors}
    logger.log_debate_complete(len(session.turns), final_scores)

    # ── 6. Export ─────────────────────────────────────────────
    if config.SAVE_TRANSCRIPT:
        filename = export_markdown(session, config.TRANSCRIPT_DIR)
        print_saved(filename)

    # ── 7. Research Kit (Academic Analysis) ────────────────────
    if config.RESEARCH_MODE:
        console.print("[dim]Đang sinh research kit...[/dim]\n")
        research_kit = generate_research_kit(session, session.topic, session.field)
        if research_kit:
            save_research_kit(research_kit, session.topic, config.RESEARCH_KIT_DIR)
            console.print("[green]✓ Research kit đã lưu[/green]\n")
    
    # ── 8. Print log file summary ─────────────────────────────
    logger.print_log_summary()


def main():
    console.print("\n[bold bright_blue]Academic Debate Arena[/bold bright_blue]\n")

    if len(sys.argv) >= 3:
        topic, field = sys.argv[1], sys.argv[2]
    else:
        field = Prompt.ask("[cyan]Lĩnh vực nghiên cứu[/cyan]",
                           default="Distributed / Efficient LLM")
        topic = Prompt.ask("[cyan]Câu hỏi tranh luận[/cyan]",
                           default="Tensor Parallelism vs Pipeline Parallelism vs MoE: đâu là chiến lược tối ưu?")

    run_debate(topic, field)


if __name__ == "__main__":
    main()
