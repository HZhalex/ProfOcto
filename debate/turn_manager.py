"""
TurnManager - manages speaking order and detects repetitive loops.
"""
from debate.session import DebateSession, ProfessorProfile


class TurnManager:
    def __init__(self, session: DebateSession):
        self.session = session
        self._idx = 0                    # current professor index
        self._repeat_count: dict[str, int] = {}  # count repetitions per professor

    # ── Lấy professor tiếp theo ───────────────────────────────────────────────

    def next_professor(self) -> ProfessorProfile:
        """Return the next professor in round-robin order."""
        profs = self.session.professors
        prof = profs[self._idx % len(profs)]
        self._idx += 1
        return prof

    def peek_next(self) -> ProfessorProfile:
        """Preview next professor without advancing index."""
        return self.session.professors[self._idx % len(self.session.professors)]

    # ── Phát hiện vòng lặp ───────────────────────────────────────────────────

    def is_repeating(self, content: str, speaker_key: str, threshold: float = 0.6) -> bool:
        """
        Kiểm tra xem professor có đang lặp lại ý đã nói không.
        Dùng simple word overlap — không cần thư viện ngoài.
        """
        # Lấy các lượt nói trước của professor này
        prev_turns = [
            t.content for t in self.session.turns
            if t.speaker_key == speaker_key and not t.is_moderator
        ]
        if not prev_turns:
            return False

        words_new = set(content.lower().split())
        for prev in prev_turns[-2:]:  # only check last 2 turns
            words_prev = set(prev.lower().split())
            if not words_prev:
                continue
            overlap = len(words_new & words_prev) / len(words_prev)
            if overlap > threshold:
                self._repeat_count[speaker_key] = self._repeat_count.get(speaker_key, 0) + 1
                return True

        return False

    def get_repeat_count(self, speaker_key: str) -> int:
        return self._repeat_count.get(speaker_key, 0)

    # ── Kiểm tra điều kiện dừng ───────────────────────────────────────────────

    def should_end_round(self, turns_this_round: int) -> bool:
        """Kết thúc round nếu đủ turns hoặc tất cả đã nói."""
        import config
        return turns_this_round >= len(self.session.professors) * config.MAX_TURNS_PER_ROUND

    def should_end_debate(self) -> bool:
        """End debate if enough rounds have been completed."""
        import config
        return self.session.current_round >= config.MAX_ROUNDS

    # ── Stats ──────────────────────────────────────────────────────────────────

    def get_stats(self) -> dict:
        """Get statistics of speaking turns for each professor."""
        counts = {}
        for t in self.session.turns:
            if not t.is_moderator:
                counts[t.speaker_name] = counts.get(t.speaker_name, 0) + 1
        return counts
