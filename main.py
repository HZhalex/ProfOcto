#!/usr/bin/env python3
"""
Academic Debate Arena
Chạy: python main.py
"""
import sys
import os

# Thêm project root vào path
sys.path.insert(0, os.path.dirname(__file__))

from rich.console import Console
from rich.prompt import Prompt

import config
from orchestrator import create_session, generate_opening_question
from agents.professor import generate_professor_turn
from agents.moderator import generate_moderator_summary, generate_final_summary
from agents.fact_checker import fact_check_turn
from debate.session import Turn
from output.terminal_renderer import (
    console,
    print_header,
    print_professors_table,
    print_round_header,
    print_moderator_turn,
    print_professor_header,
    print_fact_tags,
    print_final_summary,
    print_saved,
    stream_write,
)


def run_debate(topic: str, field: str):

    # ── 1. Setup ──────────────────────────────────────────────
    print_header(topic, field)

    console.print("[dim]Đang tạo professor profiles...[/dim]")
    session = create_session(topic, field)
    print_professors_table(session.professors)

    # ── 2. Opening ────────────────────────────────────────────
    console.print("[dim]Moderator đang chuẩn bị...[/dim]\n")
    opening = generate_opening_question(topic, session.professors)

    turn = Turn(
        turn_number=session.current_turn,
        speaker_key="moderator",
        speaker_name="Moderator",
        role="Moderator",
        content=opening,
        is_moderator=True,
    )
    session.add_turn(turn)
    print_moderator_turn(opening, turn.turn_number, "Moderator — Mở màn")

    # ── 3. Main debate loop ───────────────────────────────────
    for round_num in range(1, config.MAX_ROUNDS + 1):
        session.current_round = round_num
        print_round_header(round_num)

        for _ in range(config.MAX_TURNS_PER_ROUND):
            for prof in session.professors:

                turn_num = session.current_turn
                print_professor_header(prof, turn_num, session.professors)

                # Stream professor response
                full_text = ""
                if config.STREAM_OUTPUT:
                    console.print()  # newline trước khi stream
                    def make_callback():
                        buf = []
                        def cb(text):
                            buf.append(text)
                            stream_write(text)
                        def get():
                            return "".join(buf)
                        return cb, get
                    cb, get_text = make_callback()
                    generate_professor_turn(prof, session, stream_callback=cb)
                    full_text = get_text()
                    console.print("\n")  # newline sau khi stream xong
                else:
                    full_text = generate_professor_turn(prof, session)
                    console.print(full_text)
                    console.print()

                # Fact-check
                fact_tags = fact_check_turn(full_text, prof.name)
                if fact_tags:
                    print_fact_tags(fact_tags)
                    console.print()

                # Lưu turn vào session
                turn = Turn(
                    turn_number=turn_num,
                    speaker_key=prof.key,
                    speaker_name=prof.name,
                    role=prof.role,
                    content=full_text,
                    fact_tags=fact_tags,
                )
                session.add_turn(turn)

        # ── Moderator tóm tắt sau mỗi round ──
        if round_num < config.MAX_ROUNDS:
            console.print("[dim]Moderator đang tóm tắt...[/dim]")
            summary = generate_moderator_summary(session)
            mod_turn = Turn(
                turn_number=session.current_turn,
                speaker_key="moderator",
                speaker_name="Moderator",
                role="Moderator",
                content=summary,
                is_moderator=True,
            )
            session.add_turn(mod_turn)
            print_moderator_turn(summary, mod_turn.turn_number, f"Moderator — Tóm tắt Round {round_num}")

    # ── 4. Final summary ──────────────────────────────────────
    console.print("[dim]Đang tổng kết...[/dim]\n")
    final = generate_final_summary(session)
    print_final_summary(final)

    # ── 5. Save ───────────────────────────────────────────────
    if config.SAVE_TRANSCRIPT:
        filename = session.save_transcript(config.TRANSCRIPT_DIR)
        print_saved(filename)


def main():
    console.print("\n[bold bright_blue]Academic Debate Arena[/bold bright_blue]\n")

    if len(sys.argv) >= 3:
        topic = sys.argv[1]
        field = sys.argv[2]
    else:
        field = Prompt.ask(
            "[cyan]Lĩnh vực nghiên cứu[/cyan]",
            default="Distributed / Efficient LLM"
        )
        topic = Prompt.ask(
            "[cyan]Câu hỏi tranh luận[/cyan]",
            default="Tensor Parallelism vs Pipeline Parallelism vs MoE: đâu là chiến lược tối ưu để scale LLM lên hàng nghìn tỷ tham số?"
        )

    run_debate(topic, field)


if __name__ == "__main__":
    main()
