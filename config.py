import os

# Tự động đọc .env nếu có
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

MODEL = "gemini-2.5-flash-lite"

# Debate settings
NUM_PROFESSORS = 2    # số giáo sư, min 2 max 5
MAX_TURNS_PER_ROUND = 1
MAX_ROUNDS = 2
MAX_TOKENS_PER_TURN = 400
FACT_CHECK_ENABLED = True
LANGUAGE = "vi"

# Research Mode (khi ON: generate research kit + paper outline sau debate)
RESEARCH_MODE = True  # Bật research synthesis + paper outline
RESEARCH_MAX_RECOMMENDATIONS = 5

# Academic Rigor Mode (khi ON: professors must back claims with theorems + citations)
ACADEMIC_RIGOR_MODE = True  # Enforce mathematical backing in debates

# Mathematical Rigor Scoring (NEW - PhD focus)
THEOREM_EXTRACTION_ENABLED = True  # Extract theorems, proofs, formulas
RIGOR_SCORING_ENABLED = True  # Score each turn by math backing (0-10)
RESEARCH_GAP_DETECTION_ENABLED = True  # Identify PhD-level research gaps

# PhD Guidance Features
PhD_RECOMMENDATIONS_ENABLED = True  # Generate PhD research directions after debate
SHOW_RIGOR_SCORES = True  # Display mathematical rigor scores for each turn
DETAILED_THEOREM_ANALYSIS = True  # Show theorem breakdowns

# Display
STREAM_OUTPUT = True
SAVE_TRANSCRIPT = True
TRANSCRIPT_DIR = "transcripts"
RESEARCH_KIT_DIR = "research_kits"  # Nơi lưu research kits

# PhD Analysis Output Directory
PhD_ANALYSIS_DIR = "phd_analysis"  # Nơi lưu rigor scores, gaps, recommendations

# ICLR READINESS PIPELINE (Phase 5 - NEW)
# This pipeline: Gap → Formal Problem → Novelty → Solution Sketch → ICLR Readiness
GAP_TO_FORMAL_PROBLEM_ENABLED = True  # Convert informal gaps to formal problem statements
NOVELTY_ANALYZER_ENABLED = True  # Assess novelty vs SOTA (0-100 ICLR score)
SOLUTION_SKETCH_ENABLED = True  # Generate proof strategies from debate
ICLR_READINESS_ENABLED = True  # Complete PhD pursuit readiness assessment

# ICLR Readiness thresholds
ICLR_NOVELTY_THRESHOLD = 60  # Minimum novelty score to consider
ICLR_FEASIBILITY_THRESHOLD = 50  # Minimum feasibility score
ICLR_EVIDENCE_QUALITY_THRESHOLD = 0.5  # Minimum evidence quality (0-1)
ICLR_OVERALL_THRESHOLD = 50  # Minimum overall readiness score to recommend

# Display ICLR features
SHOW_FORMAL_PROBLEMS = True  # Display formalized problem statements
SHOW_NOVELTY_ANALYSIS = True  # Display novelty vs SOTA comparison
SHOW_SOLUTION_SKETCHES = True  # Display proof strategies
SHOW_ICLR_READINESS = True  # Display final readiness assessment
SHOW_ACTION_ITEMS = True  # Display concrete action items for pursuing gap
