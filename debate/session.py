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
    
    # NEW: Mathematical analysis (PhD focus)
    theorems_data: dict = field(default_factory=dict)  # From theorem_extractor
    rigor_score: dict = field(default_factory=dict)  # From rigor_scorer
    citations: list[dict] = field(default_factory=list)  # Extracted citations


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
        
        # NEW: PhD Analysis (Phase 3-4)
        self.all_rigor_scores: dict[str, list[dict]] = {}  # {professor_name: [scores]}
        self.research_gaps: list[dict] = []  # List of identified gaps
        self.phd_recommendations: str = ""  # Generated recommendations
        
        # NEW: ICLR Readiness Pipeline (Phase 5)
        self.formal_problems: list[dict] = []  # From gap_to_formal_problem
        self.novelty_assessments: list[dict] = []  # From novelty_analyzer
        self.solution_sketches: list[dict] = []  # From solution_sketch
        self.iclr_readiness_scores: list[dict] = []  # From iclr_readiness_scorer

    def add_professor(self, prof: ProfessorProfile):
        self.professors.append(prof)

    def add_turn(self, turn: Turn):
        self.turns.append(turn)
        self.current_turn += 1
    
    # NEW: PhD Analysis methods
    def add_rigor_score(self, speaker_name: str, score: dict):
        """Add rigor score for a professor's turn."""
        if speaker_name not in self.all_rigor_scores:
            self.all_rigor_scores[speaker_name] = []
        self.all_rigor_scores[speaker_name].append(score)
    
    def set_research_gaps(self, gaps: list[dict]):
        """Set identified research gaps."""
        self.research_gaps = gaps
    
    def set_phd_recommendations(self, recommendations: str):
        """Set PhD research recommendations."""
        self.phd_recommendations = recommendations
    
    def get_average_rigor_score(self, speaker_name: str) -> float:
        """Get average rigor score for a professor."""
        if speaker_name not in self.all_rigor_scores or not self.all_rigor_scores[speaker_name]:
            return 0.0
        scores = [s.get("rigor_score", 0) for s in self.all_rigor_scores[speaker_name]]
        return sum(scores) / len(scores) if scores else 0.0
    
    # NEW: ICLR Readiness Pipeline methods (Phase 5)
    def set_formal_problems(self, problems: list[dict]):
        """Set formalized problem statements from gaps."""
        self.formal_problems = problems
    
    def set_novelty_assessments(self, assessments: list[dict]):
        """Set novelty analysis results."""
        self.novelty_assessments = assessments
    
    def set_solution_sketches(self, sketches: list[dict]):
        """Set solution sketch results."""
        self.solution_sketches = sketches
    
    def set_iclr_readiness_scores(self, scores: list[dict]):
        """Set ICLR readiness assessment results."""
        self.iclr_readiness_scores = scores

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
