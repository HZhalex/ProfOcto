"""
Elevator Pitch Generator
Create quick verbal summaries of research gaps optimized for presentations/discussions.
"""

import re
from typing import Dict, Any, List
import config
from utils.logger import get_logger


class ElevatorPitchGenerator:
    """Generate concise pitches for research gaps."""
    
    def __init__(self, seconds: int = None):
        self.target_seconds = seconds or config.ELEVATOR_PITCH_SECONDS
        # Average speaking speed: 150 words per minute = 2.5 words per second
        self.target_words = max(30, int(self.target_seconds * 2.5))
    
    def generate_pitch(self, gap_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate elevator pitch from gap analysis.
        
        Returns:
            {
                "short": "15-30 second pitch",
                "medium": "30-60 second pitch",
                "detailed": "Full explanation with next steps",
                "bullet_points": ["Point 1", "Point 2", ...]
            }
        """
        gap_title = gap_data.get("gap_title", "Unknown gap")
        problem = gap_data.get("problem_statement", "")
        novelty = gap_data.get("novelty_score", 0)
        feasibility = gap_data.get("feasibility_assessment", {}).get("feasibility_score", 0)
        timeline = gap_data.get("timeline_assessment", {}).get("total_timeline_months", 0)
        recommendation = gap_data.get("recommendation", "").lower()
        key_innovations = gap_data.get("key_innovations", [])
        
        # Clean up problem statement
        problem_clean = self._clean_text(problem)[:100] if problem else "gap in current research"
        
        # Determine innovativeness level
        innovation_level = "incremental"
        if novelty > 75:
            innovation_level = "groundbreaking"
        elif novelty > 60:
            innovation_level = "significant"
        elif novelty > 45:
            innovation_level = "novel"
        
        # Timeline description
        timeline_desc = "within months"
        if timeline > 24:
            timeline_desc = "12+ months"
        elif timeline > 12:
            timeline_desc = "6-12 months"
        elif timeline > 6:
            timeline_desc = "3-6 months"
        
        # Build pitches of varying lengths
        short_pitch = self._build_short_pitch(gap_title, problem_clean, innovation_level, timeline_desc)
        medium_pitch = self._build_medium_pitch(gap_title, problem_clean, novelty, feasibility, timeline_desc, key_innovations)
        detailed_pitch = self._build_detailed_pitch(gap_data, innovation_level)
        bullets = self._build_bullet_points(gap_data, innovation_level)
        
        return {
            "short": short_pitch,
            "medium": medium_pitch,
            "detailed": detailed_pitch,
            "bullet_points": bullets,
            "metadata": {
                "seconds": self.target_seconds,
                "word_count": len(short_pitch.split()),
                "innovation_level": innovation_level
            }
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for presentation."""
        # Remove excessive punctuation and special chars
        text = re.sub(r'[^\w\s\-\.]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _build_short_pitch(self, gap: str, problem: str, innovation: str, timeline: str) -> str:
        """Build 15-30 second pitch (40-75 words)."""
        return f"""This research gap addresses {problem}. 
        By tackling this {innovation} opportunity, we can advance the field in {timeline}.
        The innovation lies in developing novel approaches that overcome current limitations."""
    
    def _build_medium_pitch(self, gap: str, problem: str, novelty: int, feasibility: int, timeline: str, innovations: List[str]) -> str:
        """Build 30-60 second pitch (75-150 words)."""
        feasibility_desc = "highly feasible" if feasibility > 70 else "moderately feasible" if feasibility > 50 else "challenging"
        
        pitch = f"""Our research gap: {problem}.

Current state: Existing approaches lack {problem}. By exploring this gap, we contribute {int(novelty)}% novelty to the field.

Innovation strategy: """
        
        if innovations:
            pitch += f"Focus on {', '.join(innovations[:2])}. "
        
        pitch += f"""The problem is {feasibility_desc}, solvable in {timeline}.

Why it matters: Solving this enables new applications and advances our understanding of the field."""
        
        return pitch
    
    def _build_detailed_pitch(self, gap_data: Dict[str, Any], innovation_level: str) -> str:
        """Build comprehensive explanation."""
        gap_title = gap_data.get("gap_title", "Unknown")
        problem = gap_data.get("problem_statement", "")
        novelty = gap_data.get("novelty_score", 0)
        timeline = gap_data.get("timeline_assessment", {}).get("total_timeline_months", 0)
        key_risks = gap_data.get("key_risks", [])[:2]
        next_steps = gap_data.get("next_steps_for_researcher", [])[:2]
        
        pitch = f"""RESEARCH GAP: {gap_title}

PROBLEM DEFINITION:
{self._clean_text(problem)}

INNOVATION LEVEL: {innovation_level.capitalize()} ({novelty}% novelty)

TIMELINE: {timeline} months across all research phases

KEY RISKS:
"""
        for i, risk in enumerate(key_risks, 1):
            pitch += f"{i}. {risk}\n"
        
        pitch += "\nNEXT STEPS:\n"
        for i, step in enumerate(next_steps, 1):
            pitch += f"{i}. {step}\n"
        
        pitch += f"\nRECOMMENDATION: {gap_data.get('recommendation', 'Proceed with caution and thorough planning.')}"
        
        return pitch
    
    def _build_bullet_points(self, gap_data: Dict[str, Any], innovation_level: str) -> list:
        """Build bullet-point summary."""
        bullets = [
            f"🎯 Gap: {gap_data.get('gap_title', 'Unknown')[:50]}",
            f"📊 Novelty Score: {gap_data.get('novelty_score', 0)}/100",
            f"⚙️ Innovation Level: {innovation_level}",
            f"⏱️ Timeline: {gap_data.get('timeline_assessment', {}).get('total_timeline_months', 'Unknown')} months",
            f"📈 Readiness: {gap_data.get('iclr_readiness_score', 0)}/100"
        ]
        
        feasibility = gap_data.get("feasibility_assessment", {}).get("feasibility_score", 0)
        if feasibility:
            bullets.append(f"✅ Feasibility: {feasibility}%")
        
        recommendation = gap_data.get("recommendation", "").split(".")[0]
        if recommendation:
            bullets.append(f"💡 Recommendation: {recommendation}")
        
        return bullets


def generate_elevator_pitch(gap_data: Dict[str, Any], seconds: int = None) -> Dict[str, str]:
    """Generate elevator pitch for a gap."""
    generator = ElevatorPitchGenerator(seconds=seconds)
    return generator.generate_pitch(gap_data)


def format_pitch_for_display(pitch_data: Dict[str, str], format_type: str = "short") -> str:
    """Format pitch for terminal display."""
    if format_type == "short":
        return pitch_data.get("short", "")
    elif format_type == "medium":
        return pitch_data.get("medium", "")
    elif format_type == "detailed":
        return pitch_data.get("detailed", "")
    elif format_type == "bullets":
        return "\n".join(pitch_data.get("bullet_points", []))
    else:
        return str(pitch_data)
