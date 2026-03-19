# Configuration Reference

Complete reference for all configuration flags in `config.py`. All settings have sensible defaults — most users only need to set `GEMINI_API_KEY` in their `.env` file.

---

## Table of Contents

- [AI Model](#ai-model)
- [Debate Settings](#debate-settings)
- [Research & Academic Rigor](#research--academic-rigor)
- [ICLR Readiness Pipeline (Phase 5)](#iclr-readiness-pipeline-phase-5)
- [Caching & Performance (Phase 6)](#caching--performance-phase-6)
- [Phase 5 Export & Visualization](#phase-5-export--visualization)
- [PhD UX — Startup (Phase 7)](#phd-ux--startup-phase-7)
- [PhD UX — Output Style](#phd-ux--output-style)
- [PhD UX — Feature Toggles](#phd-ux--feature-toggles)
- [PhD UX — Cost Management](#phd-ux--cost-management)
- [PhD UX — Dashboard](#phd-ux--dashboard)
- [PhD UX — Bookmarking & History](#phd-ux--bookmarking--history)
- [PhD UX — Advisor Export](#phd-ux--advisor-export)
- [PhD UX — Elevator Pitch](#phd-ux--elevator-pitch)
- [PhD UX — Batch Mode](#phd-ux--batch-mode)
- [PhD UX — Preferences](#phd-ux--preferences)
- [File Paths](#file-paths)
- [Preset Configurations](#preset-configurations)

---

## AI Model

```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")   # Loaded from .env file
MODEL = "gemma-3-1b-it"                                 # Default model (free tier)
LANGUAGE = "en"                                          # All responses in English
```

The `GEMINI_API_KEY` must be set, either via the `.env` file or as an environment variable. Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

You can change `MODEL` to any Gemini-compatible model identifier. The default `gemma-3-1b-it` is the fastest free-tier option.

---

## Debate Settings

```python
NUM_PROFESSORS = 2              # Number of professors in the panel (2–5)
MAX_TURNS_PER_ROUND = 1         # Number of turns per professor per round
MAX_ROUNDS = 1                  # Total debate rounds
MAX_TOKENS_PER_TURN = 700       # Maximum tokens per professor response
FACT_CHECK_ENABLED = True       # Fact-check each turn via web search
```

**Notes:**

- More professors and rounds produce richer debates but consume more API calls
- `MAX_TOKENS_PER_TURN = 700` is set high to allow mathematical rigor (theorems, proofs)
- With fact-checking enabled, each professor turn triggers an additional API call for verification

---

## Research & Academic Rigor

```python
# Research synthesis
RESEARCH_MODE = True                    # Generate research kit after debate
RESEARCH_MAX_RECOMMENDATIONS = 5        # Maximum number of PhD recommendations

# Academic rigor enforcement
ACADEMIC_RIGOR_MODE = True              # Require mathematical backing in responses
THEOREM_EXTRACTION_ENABLED = True       # Extract theorems, lemmas, proofs from debate
RIGOR_SCORING_ENABLED = True            # Score each turn for mathematical rigor (0–10)
RESEARCH_GAP_DETECTION_ENABLED = True   # Identify PhD-level research gaps
PhD_RECOMMENDATIONS_ENABLED = True      # Generate PhD research directions

# Display options
SHOW_RIGOR_SCORES = True                # Display rigor scores during debate
DETAILED_THEOREM_ANALYSIS = True        # Show theorem breakdowns per turn
```

**Rigor scoring breakdown:**

| Component           | Weight | Description                                       |
| ------------------- | ------ | ------------------------------------------------- |
| Theorem citations   | 35%    | References to formal theorems and lemmas          |
| Proof density       | 30%    | Presence of mathematical proofs or proof sketches |
| Citation quality    | 20%    | Quality and relevance of academic citations       |
| Logical consistency | 15%    | Internal consistency of arguments                 |

**Rigor verdicts:** HIGHLY_RIGOROUS, RIGOROUS, MODERATELY_BACKED, OPINION_BASED, UNSUPPORTED

---

## ICLR Readiness Pipeline (Phase 5)

These features are **disabled by default** because they are resource-intensive (multiple additional API calls per gap).

### Enable/Disable

```python
GAP_TO_FORMAL_PROBLEM_ENABLED = False   # Convert gaps to formal problem statements
NOVELTY_ANALYZER_ENABLED = False        # Assess novelty vs SOTA (0–100)
SOLUTION_SKETCH_ENABLED = False         # Generate proof strategies
ICLR_READINESS_ENABLED = False          # Complete readiness scoring
```

### Thresholds

```python
ICLR_NOVELTY_THRESHOLD = 60            # Minimum novelty score to recommend
ICLR_FEASIBILITY_THRESHOLD = 50        # Minimum feasibility score
ICLR_EVIDENCE_QUALITY_THRESHOLD = 0.5  # Minimum evidence quality (0–1)
ICLR_OVERALL_THRESHOLD = 50            # Minimum overall readiness score
```

### Display

```python
SHOW_FORMAL_PROBLEMS = True             # Show formalized problem statements
SHOW_NOVELTY_ANALYSIS = True            # Show novelty scores
SHOW_SOLUTION_SKETCHES = True           # Show proof strategies
SHOW_ICLR_READINESS = True             # Show readiness scores
SHOW_ACTION_ITEMS = True                # Show recommended action items
```

---

## Caching & Performance (Phase 6)

```python
CACHE_PHASE5_RESULTS = True             # Cache Gemini API results to disk
CACHE_DIR = "phd_analysis/.cache"       # Cache directory location
CACHE_MAX_SIZE = 500                    # Maximum cached items (LRU eviction)
USE_RETRY_CACHE = True                  # Enable LRU in-memory cache
```

Caching yields approximately **60% cost savings** on repeated or similar analyses. Cached results are stored as hashed files on disk and persist across sessions.

---

## Phase 5 Export & Visualization

```python
EXPORT_PHASE5_JSON = True               # Export Phase 5 results to JSON
EXPORT_PHASE5_HTML = True               # Export Phase 5 results to HTML
EXPORT_INCLUDE_DETAILED_ANALYSIS = True # Include full analysis in exports
EXPORT_AUTO_OPEN_HTML = False           # Auto-open HTML in browser after export
ENABLE_INTERACTIVE_REFINEMENT = True    # Enable interactive gap exploration menu
ENABLE_GAP_COMPARISON = True            # Enable gap comparison tables
```

---

## PhD UX — Startup (Phase 7)

```python
QUICK_START_MODE = True                 # Skip setup questions, just ask for topic
INTERACTIVE_SETUP = True                # Allow refining settings inline after quick start
```

When `QUICK_START_MODE` is enabled, ProfOcto asks only for your research topic and uses defaults for everything else. If `INTERACTIVE_SETUP` is also enabled, you get an optional prompt to adjust settings before the debate starts.

---

## PhD UX — Output Style

```python
MINIMAL_OUTPUT = False                  # Suppress verbose output
DETAILED_OUTPUT = True                  # Allow detailed output sections
SHOW_PROGRESS_BARS = True              # Show progress bars during Phase 5
VERBOSE_LOGGING = False                 # Log to console in addition to log files
```

---

## PhD UX — Feature Toggles

```python
ESTIMATE_API_COST = True                # Show cost estimate before running
SHOW_TOP_GAP_DASHBOARD = True          # Highlight the #1 recommended gap
SHOW_STATISTICS_DASHBOARD = True        # Show score averages across gaps
ENABLE_BOOKMARKING = True               # Save favorite gaps for later
ENABLE_RUN_HISTORY = True               # Track past debate sessions
ENABLE_PDF_EXPORT = True                # Export reports for advisor
ENABLE_ELEVATOR_PITCH = True            # Generate verbal summaries
ENABLE_BATCH_MODE = True                # Process multiple topics from CSV
```

---

## PhD UX — Cost Management

```python
ESTIMATE_API_COST = True                # Show projected cost before execution
COST_CONFIRMATION_THRESHOLD = 0.50      # Ask for confirmation if cost exceeds this (USD)
ESTIMATE_RUNTIME = True                 # Show projected runtime
COST_PER_API_CALL = 0.001              # Estimated cost per API call (USD)
SKIP_IF_COST_EXCEEDS = None            # Auto-skip if cost exceeds this value (None = never)
DEFAULT_NUM_GAPS = 5                    # Default gap count for cost estimation
```

---

## PhD UX — Dashboard

```python
SHOW_TOP_GAP_DASHBOARD = True          # Show #1 recommended gap prominently
SHOW_STATISTICS_DASHBOARD = True        # Show average scores across all gaps
DASHBOARD_TOP_N = 3                     # Number of top gaps to display
DASHBOARD_MINIMAL_VIEW = False          # Compact dashboard layout
```

---

## PhD UX — Bookmarking & History

```python
ENABLE_BOOKMARKING = True               # Save favorite gaps with notes
BOOKMARK_FILE = "phd_analysis/bookmarks.json"   # Bookmark storage location
ENABLE_RUN_HISTORY = True               # Track all debate sessions
HISTORY_FILE = "phd_analysis/run_history.json"   # History storage location
MAX_HISTORY_ENTRIES = 50                # Maximum number of entries to keep
```

---

## PhD UX — Advisor Export

```python
ENABLE_PDF_EXPORT = True                # Enable advisor report export
PDF_INCLUDE_TRACE = False               # Include debug trace in export
ADVISOR_EXPORT_DIR = "phd_analysis/advisor_reports"  # Export directory
```

Exports are available in TXT, HTML, and JSON formats.

---

## PhD UX — Elevator Pitch

```python
ENABLE_ELEVATOR_PITCH = True            # Enable pitch generation
ELEVATOR_PITCH_SECONDS = 15             # Default duration: 15, 30, or 60 seconds
```

---

## PhD UX — Batch Mode

```python
ENABLE_BATCH_MODE = True                # Enable multi-topic batch processing
BATCH_FILE = None                       # Path to CSV file (None = prompt user)
BATCH_RESULTS_DIR = "phd_analysis/batch_results"  # Output directory
BATCH_SKIP_DUPLICATE_TOPICS = True      # Skip previously processed topics
```

CSV format:

```csv
topic,field
"Transformer efficiency optimization","NLP"
"MoE scaling strategies","Distributed Systems"
```

---

## PhD UX — Preferences

```python
LANGUAGE_MIXED_MODE = False             # Mixed language mode
COLOR_THEME = "purple"                  # Terminal theme: "purple", "blue", or "green"
AUTO_SAVE_RESULTS = True                # Auto-save without asking
```

---

## File Paths

```python
# Output directories
STREAM_OUTPUT = True                    # Stream responses in real-time
SAVE_TRANSCRIPT = True                  # Save debate transcript to file
TRANSCRIPT_DIR = "transcripts"          # Debate transcript location
RESEARCH_KIT_DIR = "research_kits"      # Research kit output location
PhD_ANALYSIS_DIR = "phd_analysis"       # PhD analysis output directory

# Skip optional phases
SKIP_RESEARCH_KIT = False               # Skip research kit generation
SKIP_RIGOR_SCORING = False              # Skip rigor analysis
SKIP_FACT_CHECK = False                 # Skip fact-checking
FAST_MODE = False                       # Skip all optional features for speed
```

---

## Preset Configurations

### Maximum Speed

Skip optional features, minimize API calls:

```python
QUICK_START_MODE = True
FAST_MODE = True
SKIP_RESEARCH_KIT = True
NUM_PROFESSORS = 2
MAX_ROUNDS = 1
USE_RETRY_CACHE = True
```

### Budget-Conscious

Maximize quality while controlling cost:

```python
USE_RETRY_CACHE = True
COST_CONFIRMATION_THRESHOLD = 0.25
NUM_PROFESSORS = 2
MAX_ROUNDS = 1
```

### Full Analysis

Enable all features for thorough research:

```python
QUICK_START_MODE = True
NUM_PROFESSORS = 3
MAX_ROUNDS = 2
GAP_TO_FORMAL_PROBLEM_ENABLED = True
NOVELTY_ANALYZER_ENABLED = True
SOLUTION_SKETCH_ENABLED = True
ICLR_READINESS_ENABLED = True
USE_RETRY_CACHE = True
SHOW_TOP_GAP_DASHBOARD = True
```

### Development / Testing

Fast iteration with minimal output:

```python
QUICK_START_MODE = True
NUM_PROFESSORS = 2
MAX_ROUNDS = 1
MAX_TOKENS_PER_TURN = 200
MINIMAL_OUTPUT = True
STREAM_OUTPUT = False
```

---

## Tips

1. **Always enable caching** — `USE_RETRY_CACHE = True` provides ~60% cost savings
2. **Use quick start** — Most sessions only need topic input
3. **Set a cost threshold** — `COST_CONFIRMATION_THRESHOLD` prevents surprise API spending
4. **Start with defaults** — Run a quick debate first, then enable Phase 5 for promising topics
5. **Use fast mode for exploration** — Switch to full analysis once you have a strong candidate gap

---

## Common Issues

### API cost is too high

- Enable caching: `USE_RETRY_CACHE = True`
- Reduce panel size: `NUM_PROFESSORS = 2`
- Use fast mode: `FAST_MODE = True`
- Disable Phase 5 pipeline (disabled by default)

### Debates are too long

- Reduce rounds: `MAX_ROUNDS = 1`
- Reduce response length: `MAX_TOKENS_PER_TURN = 300`
- Enable fast mode: `FAST_MODE = True`

### Dashboard not showing results

- Ensure `SHOW_TOP_GAP_DASHBOARD = True`
- Ensure `RESEARCH_GAP_DETECTION_ENABLED = True`
- Check that at least 2 gaps were identified in the debate

---

**See also:**

- [Quick Start](../guides/01_QUICK_START.md) — Get running in 5 minutes
- [Feature Guide](../guides/03_PHASE7_USER_GUIDE.md) — Complete feature walkthrough
