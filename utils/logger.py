"""
Unified logging system for PhD Research Assistant.

Logs all API calls, extractions, errors to files + console.
Easier debugging when things go wrong.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class DebateLogger:
    """Centralized logger for debate sessions."""
    
    def __init__(self, session_name: str, log_dir: str = "logs"):
        """
        Initialize logger for a debate session.
        
        Args:
            session_name: Name of debate session (e.g., "Tensor_Parallelism_20260317")
            log_dir: Directory to store logs
        """
        os.makedirs(log_dir, exist_ok=True)
        
        self.session_name = session_name
        self.log_dir = log_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Main session log
        self.session_log_file = os.path.join(
            log_dir, f"session_{session_name}_{self.timestamp}.log"
        )
        
        # Sub-logs for each component
        self.theorem_log_file = os.path.join(
            log_dir, f"theorems_{session_name}_{self.timestamp}.log"
        )
        self.rigor_log_file = os.path.join(
            log_dir, f"rigor_{session_name}_{self.timestamp}.log"
        )
        self.gap_log_file = os.path.join(
            log_dir, f"gaps_{session_name}_{self.timestamp}.log"
        )
        self.error_log_file = os.path.join(
            log_dir, f"errors_{session_name}_{self.timestamp}.log"
        )
        
        # Setup loggers
        self.session_logger = self._setup_logger("session", self.session_log_file)
        self.theorem_logger = self._setup_logger("theorems", self.theorem_log_file)
        self.rigor_logger = self._setup_logger("rigor", self.rigor_log_file)
        self.gap_logger = self._setup_logger("gaps", self.gap_log_file)
        self.error_logger = self._setup_logger("errors", self.error_log_file)
    
    @staticmethod
    def _setup_logger(name: str, log_file: str) -> logging.Logger:
        """Setup logger with file and console handlers."""
        logger = logging.getLogger(f"profocto.{name}")
        logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def log_debate_start(self, topic: str, field: str, professors: list):
        """Log debate initialization."""
        self.session_logger.info(f"=== DEBATE START ===")
        self.session_logger.info(f"Topic: {topic}")
        self.session_logger.info(f"Field: {field}")
        self.session_logger.info(f"Professors: {', '.join([p.name for p in professors])}")
        self.session_logger.info(f"Timestamp: {self.timestamp}\n")
    
    def log_professor_turn(self, turn_num: int, professor_name: str, role: str):
        """Log professor's turn."""
        self.session_logger.info(f"--- Turn {turn_num} ---")
        self.session_logger.info(f"Professor: {professor_name} ({role})")
    
    # ─── THEOREM EXTRACTION LOGS ────
    def log_theorem_extraction_start(self, professor: str, content_length: int):
        """Log theorem extraction start."""
        self.theorem_logger.info(f">> Extracting theorems from {professor} (content: {content_length} chars)")
    
    def log_theorem_extraction_result(
        self,
        professor: str,
        num_theorems: int,
        num_formulas: int,
        num_assumptions: int,
        num_proofs: int,
        math_density: float
    ):
        """Log extraction results."""
        self.theorem_logger.info(f"✓ {professor} extraction complete:")
        self.theorem_logger.info(f"  - Theorems: {num_theorems}")
        self.theorem_logger.info(f"  - Formulas: {num_formulas}")
        self.theorem_logger.info(f"  - Assumptions: {num_assumptions}")
        self.theorem_logger.info(f"  - Proofs: {num_proofs}")
        self.theorem_logger.info(f"  - Math density: {math_density*100:.1f}%\n")
    
    def log_theorem_extraction_error(self, professor: str, error: Exception):
        """Log extraction error."""
        self.theorem_logger.error(f"✗ Failed to extract theorems from {professor}")
        self.theorem_logger.error(f"  Error: {str(error)}\n")
        self.error_logger.error(f"Theorem extraction | {professor} | {str(error)}", exc_info=True)
    
    def log_api_call(self, component: str, model: str, prompt_length: int):
        """Log API call."""
        self.session_logger.debug(f"API Call: {component} | Model: {model} | Prompt: {prompt_length} chars")
    
    def log_api_response(self, component: str, response_length: int, status: str = "OK"):
        """Log API response."""
        self.session_logger.debug(f"API Response: {component} | {response_length} chars | Status: {status}")
    
    # ─── RIGOR SCORING LOGS ────
    def log_rigor_scoring_start(self, professor: str):
        """Log rigor scoring start."""
        self.rigor_logger.info(f">> Scoring mathematical rigor for {professor}")
    
    def log_rigor_scoring_result(
        self,
        professor: str,
        rigor_score: float,
        verdict: str,
        breakdown: dict
    ):
        """Log scoring results."""
        self.rigor_logger.info(f"✓ {professor} scoring complete:")
        self.rigor_logger.info(f"  - Score: {rigor_score}/10")
        self.rigor_logger.info(f"  - Verdict: {verdict}")
        self.rigor_logger.info(f"  - Theorem citations:      {breakdown.get('theorem_citation_score', 0):.2f}/3")
        self.rigor_logger.info(f"  - Proof density:          {breakdown.get('proof_density_score', 0):.2f}/3")
        self.rigor_logger.info(f"  - Citation quality:       {breakdown.get('citation_quality_score', 0):.2f}/2")
        self.rigor_logger.info(f"  - Logical consistency:    {breakdown.get('logical_consistency_score', 0):.2f}/2\n")
    
    def log_rigor_scoring_error(self, professor: str, error: Exception):
        """Log scoring error."""
        self.rigor_logger.error(f"✗ Failed to score {professor}")
        self.rigor_logger.error(f"  Error: {str(error)}\n")
        self.error_logger.error(f"Rigor scoring | {professor} | {str(error)}", exc_info=True)
    
    # ─── RESEARCH GAP LOGS ────
    def log_gap_detection_start(self, num_turns: int):
        """Log gap detection start."""
        self.gap_logger.info(f">> Identifying research gaps from {num_turns} turns")
    
    def log_gap_detected(
        self,
        gap_id: int,
        gap_type: str,
        title: str,
        difficulty: str,
        phd_value: str
    ):
        """Log detected gap."""
        self.gap_logger.info(f"✓ Gap {gap_id} | {gap_type}:")
        self.gap_logger.info(f"  - Title: {title}")
        self.gap_logger.info(f"  - Difficulty: {difficulty}")
        self.gap_logger.info(f"  - PhD Value: {phd_value}")
    
    def log_gap_detection_complete(self, num_gaps: int):
        """Log gap detection complete."""
        self.gap_logger.info(f"✓ Research gap detection complete: {num_gaps} gaps identified\n")
    
    def log_gap_detection_error(self, error: Exception):
        """Log gap detection error."""
        self.gap_logger.error(f"✗ Failed to detect research gaps")
        self.gap_logger.error(f"  Error: {str(error)}\n")
        self.error_logger.error(f"Gap detection | {str(error)}", exc_info=True)
    
    # ─── GENERAL LOGS ────
    def log_debate_complete(self, num_turns: int, final_rigor_scores: dict):
        """Log debate completion."""
        self.session_logger.info(f"=== DEBATE COMPLETE ===")
        self.session_logger.info(f"Total turns: {num_turns}")
        self.session_logger.info(f"Final rigor scores:")
        for prof, score in final_rigor_scores.items():
            self.session_logger.info(f"  - {prof}: {score:.1f}/10")
        self.session_logger.info(f"Log files saved to: {self.log_dir}/")
    
    def log_warning(self, component: str, message: str):
        """Log warning."""
        self.session_logger.warning(f"[{component}] {message}")
    
    def log_error(self, component: str, error: Exception, context: Optional[str] = None):
        """Log error."""
        self.error_logger.error(f"[{component}] {str(error)}")
        if context:
            self.error_logger.error(f"  Context: {context}")
        self.error_logger.error("", exc_info=True)
    
    def log_phd_recommendations_generated(self, num_gaps: int):
        """Log PhD recommendations generation."""
        self.session_logger.info(f"✓ Generated PhD research recommendations from {num_gaps} gaps")
    
    def print_log_summary(self):
        """Print summary of logs created."""
        from rich.console import Console
        console = Console()
        
        console.print("\n[bold cyan]📋 LOG FILES CREATED[/bold cyan]\n")
        console.print(f"[dim]Session logs:[/dim] {self.session_log_file}")
        console.print(f"[dim]Theorem logs:[/dim] {self.theorem_log_file}")
        console.print(f"[dim]Rigor logs:[/dim] {self.rigor_log_file}")
        console.print(f"[dim]Gap logs:[/dim] {self.gap_log_file}")
        console.print(f"[dim]Error logs:[/dim] {self.error_log_file}")
        console.print(f"\n[dim]All logs in: {self.log_dir}/[/dim]\n")


# Global logger instance
_logger_instance: Optional[DebateLogger] = None


def init_logger(session_name: str) -> DebateLogger:
    """Initialize global logger for session."""
    global _logger_instance
    _logger_instance = DebateLogger(session_name)
    return _logger_instance


def get_logger() -> DebateLogger:
    """Get global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = DebateLogger("default")
    return _logger_instance
