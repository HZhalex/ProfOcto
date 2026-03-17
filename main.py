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
from output.phase5_exporter import export_phase5_json, export_phase5_html
from output.interactive_cli import launch_interactive_cli
from agents.gap_ranker import generate_comparison_table, identify_pareto_frontier
from utils.logger import init_logger, get_logger
from utils.retry_cache import get_cache_stats

# Phase 7: PhD UX Improvements
from output.phd_startup_cli import run_startup, PhDStartupCLI
from output.cost_estimator import estimate_cost_for_gaps, CostEstimator
from output.gap_dashboard import show_gap_dashboard
from output.elevator_pitch import generate_elevator_pitch, format_pitch_for_display
from output.pdf_exporter import export_for_advisor, export_debate_summary
from utils.bookmark_history import get_bookmark_manager, get_history_manager
from output.batch_processor import BatchProcessor


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
    # ROBUST: Handles per-gap errors, continues processing, returns partial results
    if config.ICLR_READINESS_ENABLED and session.research_gaps:
        console.print("\n[bold bright_cyan]━━━ ICLR READINESS ASSESSMENT PIPELINE ━━━[/bold bright_cyan]\n")
        
        # Phase 7: Show cost estimate before running
        if config.ESTIMATE_API_COST:
            num_gaps = len(session.research_gaps)
            estimator = CostEstimator()
            estimate = estimator.estimate_for_gaps(num_gaps)
            
            console.print(estimator.format_cost_summary(estimate))
            
            # Ask for confirmation if cost is high
            if estimator.should_confirm_cost(estimate):
                should_proceed = Prompt.ask(
                    "[bold yellow]Proceed with analysis?[/bold yellow]",
                    choices=["y", "n"],
                    default="y"
                )
                if should_proceed.lower() != "y":
                    console.print("[yellow]Analysis skipped by user.[/yellow]")
                    return
        
        # Initialize variables for each phase
        formal_problems = []
        novelty_results = []
        solution_sketches = []
        readiness_scores = []
        
        try:
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
            
            # Phase 5-1: Gap → Formal Problem (robust per-gap processing)
            if config.GAP_TO_FORMAL_PROBLEM_ENABLED and config.SHOW_FORMAL_PROBLEMS:
                console.print("[dim]→ Formalizing gaps to mathematical problems...[/dim]")
                for gap in session.research_gaps:
                    try:
                        from agents.gap_to_formal_problem import formalize_research_gap
                        formal = formalize_research_gap(gap, debate_context, session.topic)
                        formal_problems.append(formal)
                    except Exception as e:
                        logger.log_error("gap_formalization", e, context=f"Gap: {gap.get('title')}")
                        console.print(f"  [yellow]⚠ Skip gap '{gap.get('title')}': {str(e)[:60]}[/yellow]")
                
                session.set_formal_problems(formal_problems)
                console.print(f"[green]✓ Formalized {len(formal_problems)}/{len(session.research_gaps)} problems[/green]\n")
            
            # Phase 5-2: Novelty Analysis (robust per-problem)
            if config.NOVELTY_ANALYZER_ENABLED and config.SHOW_NOVELTY_ANALYSIS and formal_problems:
                console.print("[dim]→ Analyzing novelty vs SOTA...[/dim]")
                for problem in formal_problems:
                    try:
                        from agents.novelty_analyzer import score_novelty
                        result = score_novelty(problem, all_citations, debate_context, session.topic)
                        novelty_results.append(result)
                    except Exception as e:
                        logger.log_error("novelty_analysis", e, context=f"Problem: {problem.get('gap_title')}")
                        console.print(f"  [yellow]⚠ Skip novelty for '{problem.get('gap_title')}': {str(e)[:60]}[/yellow]")
                
                session.set_novelty_assessments(novelty_results)
                console.print(f"[green]✓ Analyzed {len(novelty_results)}/{len(formal_problems)} problems[/green]\n")
            
            # Phase 5-3: Solution Sketches (robust per-problem)
            if config.SOLUTION_SKETCH_ENABLED and config.SHOW_SOLUTION_SKETCHES and formal_problems:
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
                
                for problem in formal_problems:
                    try:
                        from agents.solution_sketch import generate_solution_sketch
                        sketch = generate_solution_sketch(problem, debate_context, professor_arguments)
                        solution_sketches.append(sketch)
                    except Exception as e:
                        logger.log_error("solution_sketch", e, context=f"Problem: {problem.get('gap_title')}")
                        console.print(f"  [yellow]⚠ Skip sketch for '{problem.get('gap_title')}': {str(e)[:60]}[/yellow]")
                
                session.set_solution_sketches(solution_sketches)
                console.print(f"[green]✓ Generated {len(solution_sketches)}/{len(formal_problems)} sketches[/green]\n")
            
            # Phase 5-4: ICLR Readiness Assessment (robust per-gap)
            if config.ICLR_READINESS_ENABLED and config.SHOW_ICLR_READINESS and formal_problems:
                console.print("[dim]→ Assessing ICLR readiness for PhD pursuit...[/dim]")
                
                # Match problems to novelty and sketches
                novelty_map = {n.get("gap_title"): n for n in novelty_results}
                sketch_map = {s.get("gap_title"): s for s in solution_sketches}
                
                for problem in formal_problems:
                    try:
                        from agents.iclr_readiness_scorer import assess_iclr_readiness
                        novelty = novelty_map.get(problem.get("gap_title"), {})
                        sketch = sketch_map.get(problem.get("gap_title"), {})
                        
                        assessment = assess_iclr_readiness(problem, novelty, sketch, all_rigor_scores)
                        readiness_scores.append(assessment)
                    except Exception as e:
                        logger.log_error("iclr_readiness", e, context=f"Problem: {problem.get('gap_title')}")
                        console.print(f"  [yellow]⚠ Skip readiness for '{problem.get('gap_title')}': {str(e)[:60]}[/yellow]")
                
                session.set_iclr_readiness_scores(readiness_scores)
                console.print(f"[green]✓ Assessed readiness for {len(readiness_scores)}/{len(formal_problems)} gaps[/green]\n")
                
                # Display executive summary if have results
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
            
            # Log phase 5 completion stats
            logger.gap_logger.info(f"Phase 5 complete: {len(formal_problems)} problems, {len(novelty_results)} novelty, {len(solution_sketches)} sketches, {len(readiness_scores)} readiness")
        
        except Exception as e:
            logger.log_error("iclr_pipeline", e, context="Phase 5 setup error")
            console.print(f"[red]⚠ ICLR pipeline error: {str(e)}[/red]\n")
        
        # NEW: Phase 5 Export (JSON + HTML) ─────────────────────────────
        if config.EXPORT_PHASE5_JSON and readiness_scores:
            console.print("[dim]→ Exporting Phase 5 results to JSON...[/dim]")
            try:
                export_dir = export_phase5_json(
                    session.topic,
                    formal_problems,
                    novelty_results,
                    solution_sketches,
                    readiness_scores,
                    config.PhD_ANALYSIS_DIR
                )
                console.print(f"[green]✓ JSON exported to {export_dir}[/green]")
            except Exception as e:
                logger.log_error("export_json", e, context="JSON export failed")
                console.print(f"[yellow]⚠ JSON export failed: {str(e)[:60]}[/yellow]")
        
        if config.EXPORT_PHASE5_HTML and readiness_scores:
            console.print("[dim]→ Generating HTML report...[/dim]")
            try:
                html_file = export_phase5_html(
                    session.topic,
                    readiness_scores,
                    config.PhD_ANALYSIS_DIR
                )
                console.print(f"[green]✓ HTML report: {html_file}[/green]")
                if config.EXPORT_AUTO_OPEN_HTML:
                    import webbrowser
                    webbrowser.open(f"file://{os.path.abspath(html_file)}")
            except Exception as e:
                logger.log_error("export_html", e, context="HTML export failed")
                console.print(f"[yellow]⚠ HTML export failed: {str(e)[:60]}[/yellow]")
        
        # NEW: Show Gap Comparison & Rankings ───────────────────────────
        if config.ENABLE_GAP_COMPARISON and readiness_scores and len(readiness_scores) > 1:
            console.print("\n[bold cyan]📊 GAP COMPARISON[/bold cyan]\n")
            comparison = generate_comparison_table(readiness_scores)
            console.print(comparison)
            
            # Show Pareto frontier
            frontier = identify_pareto_frontier(readiness_scores)
            if len(frontier) < len(readiness_scores):
                console.print(f"\n[bold]Pareto-optimal gaps ({len(frontier)}):[/bold]")
                for gap in frontier:
                    console.print(f"  ✓ {gap}")
        
        # NEW: Show API cache stats ──────────────────────────────────────
        if config.CACHE_PHASE5_RESULTS:
            cache_stats = get_cache_stats()
            console.print(f"\n[dim]Cache: {cache_stats['cached_items']} items, {cache_stats['total_accesses']} accesses[/dim]")
        
        # NEW: Interactive Refinement CLI ─────────────────────────────────
        if config.ENABLE_INTERACTIVE_REFINEMENT and readiness_scores:
            # Phase 7: Show dashboard first
            if config.SHOW_TOP_GAP_DASHBOARD:
                dashboard = show_gap_dashboard(readiness_scores, session.topic)
                console.print(dashboard)
            
            # Track run in history
            if config.ENABLE_RUN_HISTORY:
                history_mgr = get_history_manager()
                history_mgr.record_run(session.topic, session.field, readiness_scores)
            
            # Interactive menu with Phase 7 options
            should_interact = Prompt.ask(
                "\n[bold cyan]🔍 Explore gaps interactively?[/bold cyan]",
                choices=["y", "n"],
                default="n"
            )
            if should_interact.lower() == "y":
                console.print("\n[dim]Interactive Options:[/dim]")
                console.print("[1] View detailed gap analysis")
                
                if config.ENABLE_BOOKMARKING:
                    console.print("[2] Bookmark your favorite gap")
                
                if config.ENABLE_PDF_EXPORT:
                    console.print("[3] Export gap analysis for advisor")
                
                if config.ENABLE_ELEVATOR_PITCH:
                    console.print("[4] Generate elevator pitch")
                
                if config.ENABLE_RUN_HISTORY:
                    console.print("[5] Compare with previous runs")
                
                console.print("[0] Continue to detailed interactive mode")
                
                choice = Prompt.ask("Select option", default="0")
                
                # Phase 7: Handle new options
                if choice == "2" and config.ENABLE_BOOKMARKING:
                    gap_to_bookmark = Prompt.ask(
                        "Which gap to bookmark? (enter gap number or 0 for top gap)",
                        default="1"
                    )
                    try:
                        gap_idx = (int(gap_to_bookmark) - 1) if gap_to_bookmark != "0" else 0
                        if 0 <= gap_idx < len(readiness_scores):
                            bookmark_mgr = get_bookmark_manager()
                            bookmark_mgr.bookmark(
                                readiness_scores[gap_idx].get('gap_title'),
                                readiness_scores[gap_idx],
                                notes=Prompt.ask("Optional notes", default="")
                            )
                            console.print(f"[green]✓ Gap bookmarked![/green]")
                    except:
                        console.print("[yellow]Invalid selection[/yellow]")
                
                elif choice == "3" and config.ENABLE_PDF_EXPORT:
                    gap_to_export = Prompt.ask(
                        "Which gap to export? (enter number or 'all')",
                        default="1"
                    )
                    try:
                        if gap_to_export.lower() == "all":
                            export_debate_summary(session.topic, readiness_scores, format="txt")
                            console.print("[green]✓ Full summary exported![/green]")
                        else:
                            gap_idx = int(gap_to_export) - 1
                            if 0 <= gap_idx < len(readiness_scores):
                                filepath = export_for_advisor(readiness_scores[gap_idx], format="txt")
                                console.print(f"[green]✓ Exported to: {filepath}[/green]")
                    except:
                        console.print("[yellow]Invalid selection[/yellow]")
                
                elif choice == "4" and config.ENABLE_ELEVATOR_PITCH:
                    gap_to_pitch = Prompt.ask("Which gap? (enter number)", default="1")
                    try:
                        gap_idx = int(gap_to_pitch) - 1
                        if 0 <= gap_idx < len(readiness_scores):
                            pitch = generate_elevator_pitch(readiness_scores[gap_idx])
                            console.print("\n[bold cyan]📢 Elevator Pitch (30 sec):[/bold cyan]\n")
                            console.print(pitch['short'])
                            console.print("\n[bold cyan]Key Points:[/bold cyan]")
                            for bullet in pitch['bullet_points']:
                                console.print(f"  {bullet}")
                    except:
                        console.print("[yellow]Invalid selection[/yellow]")
                
                elif choice == "5" and config.ENABLE_RUN_HISTORY:
                    history_mgr = get_history_manager()
                    recent = history_mgr.get_recent_runs(3)
                    if len(recent) > 1:
                        console.print("\n[bold cyan]📋 Recent Runs:[/bold cyan]")
                        for i, run in enumerate(recent, 1):
                            console.print(f"  {i}. {run['topic']} ({run['run_at'][:10]})")
                        # Simple comparison logic
                        console.print(f"\n[green]✓ Showing {len(recent)} recent debates[/green]")
                
                # Launch full interactive CLI if user wants more details
                if choice == "0" or choice not in ["2", "3", "4", "5"]:
                    launch_interactive_cli(readiness_scores)
    
    
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

    # Phase 7: Hybrid startup CLI (quick by default, interactive optional)
    if config.QUICK_START_MODE or config.INTERACTIVE_SETUP:
        startup_settings = run_startup()
        topic = startup_settings['topic']
        field = startup_settings['field']
    elif len(sys.argv) >= 3:
        topic, field = sys.argv[1], sys.argv[2]
    else:
        field = Prompt.ask("[cyan]Lĩnh vực nghiên cứu[/cyan]",
                           default="Distributed / Efficient LLM")
        topic = Prompt.ask("[cyan]Câu hỏi tranh luận[/cyan]",
                           default="Tensor Parallelism vs Pipeline Parallelism vs MoE: đâu là chiến lược tối ưu?")

    run_debate(topic, field)


if __name__ == "__main__":
    main()
