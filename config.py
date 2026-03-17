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

MODEL = "gemma-3-4b-it"

# Debate settings
NUM_PROFESSORS = 2    # số giáo sư, min 2 max 5
MAX_TURNS_PER_ROUND = 1
MAX_ROUNDS = 1
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

# CACHING & OPTIMIZATION (Phase 6)
CACHE_PHASE5_RESULTS = True  # Cache Gemini API results to reduce cost/speed up re-runs
CACHE_DIR = "phd_analysis/.cache"  # Where to store cached API results
CACHE_MAX_SIZE = 500  # Maximum number of cached items
USE_RETRY_CACHE = True  # Enable LRU cache with disk persistence for API calls

# PHASE 5 EXPORT & VISUALIZATION
EXPORT_PHASE5_JSON = True  # Export Phase 5 results to JSON
EXPORT_PHASE5_HTML = True  # Generate HTML reports for visualization
EXPORT_INCLUDE_DETAILED_ANALYSIS = True  # Include full trace logs in exports
EXPORT_AUTO_OPEN_HTML = False  # Auto-open generated HTML in browser

# INTERACTIVE FEATURES
ENABLE_INTERACTIVE_REFINEMENT = True  # Allow user to refine analysis after pipeline
ENABLE_GAP_COMPARISON = True  # Show gap comparison/ranking table

# ══════════════════════════════════════════════════════════════
# PhD STUDENT UX IMPROVEMENTS (NEW)
# ══════════════════════════════════════════════════════════════

# STARTUP MODE
QUICK_START_MODE = True  # True: skip optional questions, just ask topic. False: configure everything
INTERACTIVE_SETUP = True  # Allow refining settings after quick start

# OUTPUT STYLE  
MINIMAL_OUTPUT = False  # True: only critical info. False: detailed. Can toggle interactively
DETAILED_OUTPUT = True  # Complement to MINIMAL: show both if True
SHOW_PROGRESS_BARS = True  # Show progress during Phase 5
VERBOSE_LOGGING = False  # Print all logs to console (not just file)

# SKIP OPTIONAL FEATURES (for speed)
SKIP_RESEARCH_KIT = False  # Skip research synthesis step
SKIP_RIGOR_SCORING = False  # Skip mathematical rigor analysis
SKIP_FACT_CHECK = False  # Skip fact-checking step
FAST_MODE = False  # Master toggle: skip all optional features

# COST & TIMELINE AWARENESS
ESTIMATE_API_COST = True  # Show estimated API cost before running
COST_CONFIRMATION_THRESHOLD = 0.50  # Ask user to confirm if cost > $X
ESTIMATE_RUNTIME = True  # Estimate total runtime
COST_PER_API_CALL = 0.001  # USD per Gemini API call (for estimation)
SKIP_IF_COST_EXCEEDS = None  # Skip if estimated cost > this ($ value), None = always run
DEFAULT_NUM_GAPS = 5  # Default number of gaps to analyze in cost estimation

# TOP GAP RECOMMENDATION
SHOW_TOP_GAP_DASHBOARD = True  # Show #1 recommended gap prominently after pipeline
SHOW_STATISTICS_DASHBOARD = True  # Show average scores and statistics on dashboard
DASHBOARD_TOP_N = 3  # Show top N gaps in dashboard
DASHBOARD_MINIMAL_VIEW = False  # Show minimal dashboard (just titles + scores)

# BOOKMARKING & HISTORY
ENABLE_BOOKMARKING = True  # Allow PhD to bookmark favorite gaps
BOOKMARK_FILE = "phd_analysis/bookmarks.json"  # Where to save bookmarks
ENABLE_RUN_HISTORY = True  # Track all debate runs for comparison
HISTORY_FILE = "phd_analysis/run_history.json"  # Where to save run history
MAX_HISTORY_ENTRIES = 50  # Keep last 50 runs

# PDF EXPORT FOR ADVISOR
ENABLE_PDF_EXPORT = True  # Export gap analysis as PDF
PDF_INCLUDE_TRACE = False  # Include detailed trace logs in PDF (longer)
ADVISOR_EXPORT_DIR = "phd_analysis/advisor_reports"  # Where to save advisor PDFs

# ELEVATOR PITCH GENERATOR
ENABLE_ELEVATOR_PITCH = True  # Generate 15-30 sec summaries of gaps
ELEVATOR_PITCH_SECONDS = 15  # Target duration (affects length)

# BATCH MODE
ENABLE_BATCH_MODE = True  # Run multiple debates in sequence
BATCH_FILE = None  # Path to CSV with (topic, field) pairs. None = ask user
BATCH_RESULTS_DIR = "phd_analysis/batch_results"  # Where to save batch processing results
BATCH_SKIP_DUPLICATE_TOPICS = True  # Don't re-run if cached

# PREFERENCES
LANGUAGE_MIXED_MODE = True  # Use Vietnamese for UI, English for technical terms
COLOR_THEME = "purple"  # Color scheme: "purple", "blue", "green"
AUTO_SAVE_RESULTS = True  # Auto-save results without asking
