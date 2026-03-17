"""
Gap Dashboard - Post-Pipeline Summary Display
Show top gaps prominently with quick action buttons.
"""

from typing import List, Dict, Any
import config
from utils.logger import get_logger


class GapDashboard:
    """Display top gaps after pipeline completes."""
    
    def __init__(self):
        self.logger = get_logger()
    
    def show_dashboard(self, gaps: List[Dict[str, Any]], topic: str = "") -> str:
        """
        Display top gaps in dashboard format.
        
        Args:
            gaps: List of gap analyses with readiness scores
            topic: Original research topic (for context)
            
        Returns:
            Formatted dashboard string
        """
        
        if not gaps:
            return "No gaps found to display.\n"
        
        if not config.SHOW_TOP_GAP_DASHBOARD:
            return ""
        
        # Sort by readiness score
        sorted_gaps = sorted(gaps, key=lambda x: x.get('iclr_readiness_score', 0), reverse=True)
        
        # Build dashboard
        dashboard = self._build_header(len(gaps), topic)
        dashboard += self._build_top_gap_section(sorted_gaps[0])
        
        if len(sorted_gaps) > 1:
            dashboard += self._build_top_3_section(sorted_gaps[:3])
        
        dashboard += self._build_action_buttons()
        dashboard += self._build_quick_stats(sorted_gaps)
        
        return dashboard
    
    def _build_header(self, num_gaps: int, topic: str) -> str:
        """Build dashboard header."""
        return f"""
╔{'═'*68}╗
║ {'GAP ANALYSIS DASHBOARD'.center(66)} ║
╠{'═'*68}╣
│ Topic: {topic[:50] if topic else 'General Research':<50} │
│ Total Gaps Found: {num_gaps:<46} │
╚{'═'*68}╝

"""
    
    def _build_top_gap_section(self, top_gap: Dict[str, Any]) -> str:
        """Build prominent #1 gap section."""
        gap_title = top_gap.get('gap_title', 'Unknown Gap')
        score = top_gap.get('iclr_readiness_score', 0)
        novelty = top_gap.get('novelty_score', 0)
        feasibility = top_gap.get('feasibility_assessment', {}).get('feasibility_score', 0)
        recommendation = top_gap.get('recommendation', 'Proceed with caution')
        timeline = top_gap.get('timeline_assessment', {}).get('total_timeline_months', 0)
        
        # Color coding for readiness
        if score >= 75:
            status = "✅ HIGHLY READY"
        elif score >= 60:
            status = "⚠️  READY WITH RISKS"
        elif score >= 45:
            status = "🔶 CHALLENGING"
        else:
            status = "❌ NOT RECOMMENDED"
        
        section = f"""
╔{'═'*68}╗
║ 🎯 TOP GAP #1 (RECOMMENDED FOR PURSUIT) {' '*23} ║
╠{'═'*68}╣
║ {gap_title[:66]} │
╠{'═'*68}╣
║ Status: {status:<52} ║
║ Readiness Score: {score}/100 {'█'*int(score/5):<34} ║
║ Novelty: {novelty}/100 | Feasibility: {feasibility}/100 {'█'*int((novelty+feasibility)/(100/10)):<19} ║
║ Timeline: ~{timeline} months {'(Shorter is better)':<40} ║
╠{'═'*68}╣
║ Recommendation: {' '*47} ║
"""
        
        # Wrap recommendation text
        rec_lines = self._wrap_text(recommendation, 62)
        for i, line in enumerate(rec_lines):
            if i == 0:
                section += f"║ {line:<66} ║\n"
            else:
                section += f"║ {line:<66} ║\n"
        
        section += f"╚{'═'*68}╝\n"
        
        return section
    
    def _build_top_3_section(self, top_3_gaps: List[Dict[str, Any]]) -> str:
        """Build section showing top 3 gaps."""
        section = f"""
╔{'═'*68}╗
║ {'TOP 3 GAPS OVERVIEW'.center(66)} ║
╠{'═'*68}╣
"""
        
        for i, gap in enumerate(top_3_gaps, 1):
            gap_title = gap.get('gap_title', 'Unknown')[:50]
            score = gap.get('iclr_readiness_score', 0)
            novelty = gap.get('novelty_score', 0)
            
            section += f"""║ {i}. {gap_title:<50} Readiness: {score:>3}/100 ║
"""
        
        section += f"╚{'═'*68}╝\n"
        
        return section
    
    def _build_action_buttons(self) -> str:
        """Build quick action buttons."""
        buttons = f"""
╔{'═'*68}╗
║ {'QUICK ACTIONS'.center(66)} ║
╠{'═'*68}╣
"""
        
        if config.ENABLE_BOOKMARKING:
            buttons += "║ [1] 📌 Bookmark this gap for future reference             ║\n"
        
        if config.ENABLE_PDF_EXPORT:
            buttons += "║ [2] 🚀 Export to PDF for advisor discussion              ║\n"
        
        if config.ENABLE_ELEVATOR_PITCH:
            buttons += "║ [3] 💬 Generate elevator pitch for presentation          ║\n"
        
        if config.ENABLE_RUN_HISTORY:
            buttons += "║ [4] 📋 Compare with previous analysis runs              ║\n"
        
        buttons += f"""║ [5] 🔍 View detailed analysis                          ║
╚{'═'*68}╝

"""
        
        return buttons
    
    def _build_quick_stats(self, gaps: List[Dict[str, Any]]) -> str:
        """Build quick statistics section."""
        if not config.SHOW_STATISTICS_DASHBOARD:
            return ""
        
        readiness_scores = [g.get('iclr_readiness_score', 0) for g in gaps]
        novelty_scores = [g.get('novelty_score', 0) for g in gaps]
        feasibility_scores = [g.get('feasibility_assessment', {}).get('feasibility_score', 0) for g in gaps]
        
        avg_readiness = sum(readiness_scores) / len(readiness_scores) if readiness_scores else 0
        avg_novelty = sum(novelty_scores) / len(novelty_scores) if novelty_scores else 0
        avg_feasibility = sum(feasibility_scores) / len(feasibility_scores) if feasibility_scores else 0
        
        stats = f"""
╔{'═'*68}╗
║ {'ANALYSIS STATISTICS'.center(66)} ║
╠{'═'*68}╣
║ Average Readiness:    {avg_readiness:>5.1f}/100 {'█'*int(avg_readiness/5):<33} ║
║ Average Novelty:      {avg_novelty:>5.1f}/100 {'█'*int(avg_novelty/5):<33} ║
║ Average Feasibility:  {avg_feasibility:>5.1f}/100 {'█'*int(avg_feasibility/5):<33} ║
╚{'═'*68}╝

"""
        
        return stats
    
    def _wrap_text(self, text: str, width: int = 62) -> list:
        """Wrap text to specified width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


def show_gap_dashboard(gaps: List[Dict[str, Any]], topic: str = "") -> str:
    """Convenience function to display gap dashboard."""
    dashboard = GapDashboard()
    return dashboard.show_dashboard(gaps, topic)
