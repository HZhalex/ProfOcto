from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json
import os


@dataclass
class Turn:
    turn_number: int
    speaker_key: str
    speaker_name: str
    role: str
    content: str
    fact_tags: list[dict] = field(default_factory=list)
    is_moderator: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ProfessorProfile:
    key: str
    name: str
    university: str
    role: str          # e.g. "Empiricist", "Skeptic"
    personality: str   # mô tả tính cách và phong cách tranh luận
    stance: str        # quan điểm cụ thể với topic này
    expertise: str     # chuyên môn


class DebateSession:
    def __init__(self, topic: str, field: str):
        self.topic = topic
        self.field = field
        self.professors: list[ProfessorProfile] = []
        self.turns: list[Turn] = []
        self.current_turn = 0
        self.current_round = 0
        self.started_at = datetime.now().isoformat()

    def add_professor(self, prof: ProfessorProfile):
        self.professors.append(prof)

    def add_turn(self, turn: Turn):
        self.turns.append(turn)
        self.current_turn += 1

    def get_history_text(self, max_turns: Optional[int] = None) -> str:
        """Trả về lịch sử tranh luận dạng text để truyền vào context."""
        turns = self.turns[-max_turns:] if max_turns else self.turns
        lines = []
        for t in turns:
            prefix = "[MODERATOR]" if t.is_moderator else f"[{t.speaker_name} — {t.role}]"
            lines.append(f"{prefix}\n{t.content}")
            if t.fact_tags:
                for ft in t.fact_tags:
                    lines.append(f"  • {ft['claim']} → [{ft['status'].upper()}]")
        return "\n\n".join(lines)

    def get_professors_summary(self) -> str:
        lines = []
        for p in self.professors:
            lines.append(f"- {p.name} ({p.university}) | {p.role} | Stance: {p.stance}")
        return "\n".join(lines)

    def save_transcript(self, directory: str = "transcripts"):
        os.makedirs(directory, exist_ok=True)
        slug = self.topic[:40].replace(" ", "_").replace("/", "-")
        filename = f"{directory}/debate_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        lines = [
            f"# Academic Debate Arena",
            f"**Topic:** {self.topic}",
            f"**Field:** {self.field}",
            f"**Date:** {self.started_at}",
            f"",
            f"## Professors",
        ]
        for p in self.professors:
            lines.append(f"- **{p.name}** ({p.university}) — {p.role}")
            lines.append(f"  - Stance: {p.stance}")

        lines += ["", "---", "", "## Debate Transcript", ""]

        for t in self.turns:
            if t.is_moderator:
                lines.append(f"### 🎯 Moderator — Turn {t.turn_number}")
                lines.append(f"> {t.content}")
            else:
                lines.append(f"### 👤 {t.speaker_name} ({t.role}) — Turn {t.turn_number}")
                lines.append(t.content)
                if t.fact_tags:
                    lines.append("")
                    lines.append("**Fact Check:**")
                    for ft in t.fact_tags:
                        status_emoji = {"VERIFIED": "✅", "UNVERIFIED": "⚠️", "OPINION": "💭", "CONTESTED": "🔴"}.get(ft["status"].upper(), "❓")
                        lines.append(f"- {status_emoji} `{ft['status'].upper()}` — {ft['claim']}")
            lines.append("")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return filename
