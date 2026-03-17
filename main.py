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
from debate.session import Turn
from debate.turn_manager import TurnManager
from output.terminal_renderer import (
    console, print_header, print_professors_table, print_round_header,
    print_moderator_turn, print_professor_header, print_fact_tags,
    print_final_summary, print_saved, stream_write,
)
from output.exporter import export_markdown


def run_debate(topic: str, field: str):

    # ── 1. Setup ──────────────────────────────────────────────
    print_header(topic, field)
    console.print("[dim]Đang tạo professor profiles...[/dim]")
    session = create_session(topic, field)
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

                # Lưu turn
                session.add_turn(Turn(
                    turn_number=turn_num, speaker_key=prof.key,
                    speaker_name=prof.name, role=prof.role,
                    content=full_text, fact_tags=fact_tags,
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
