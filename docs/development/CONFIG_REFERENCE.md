# Configuration Reference

Complete guide to all 100+ configuration flags in `config.py`.

## Organization

Flags are organized by feature area:

- [Debate Settings](#debate-settings)
- [Research & Rigor](#research--rigor)
- [Phase 5: ICLR Pipeline](#phase-5-iclr-pipeline)
- [Phase 7: PhD UX](#phase-7-phd-ux)
- [Caching & Performance](#caching--performance)
- [Display & Output](#display--output)
- [File Paths](#file-paths)

---

## AI Model Settings

```python
# Choose AI model (all free tier)
MODEL = "gemini-2.0-flash"      # Options: "gemini-2.0-flash" (default, fastest)
                                #          "gemini-1.5-flash" (balanced)
                                #          "gemini-1.5-pro" (highest quality, limited)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # From .env file
LANGUAGE = "en"                 # Enforce English responses
```

**Free Tier Rate Limits:**

- 15 requests per minute
- 1,000,000 tokens per minute
- Resets daily

**Model Comparison:**

| Model              | Speed  | Quality    | Best For                     | Max Context |
| ------------------ | ------ | ---------- | ---------------------------- | ----------- |
| `gemini-2.0-flash` | ⚡⚡⚡ | ⭐⭐⭐     | Fast debates, quick feedback | 1M tokens   |
| `gemini-1.5-flash` | ⚡⚡   | ⭐⭐⭐⭐   | Balanced performance         | 1M tokens   |
| `gemini-1.5-pro`   | ⚡     | ⭐⭐⭐⭐⭐ | Rigorous PhD debates         | 2M tokens   |

---

## Debate Settings

```python
NUM_PROFESSORS = 2              # Number of professors (2-5, more = more expensive)
MAX_ROUNDS = 2                  # Debate rounds
MAX_TURNS_PER_ROUND = 1         # Turns per professor per round
MAX_TOKENS_PER_TURN = 700       # Max tokens per response (increased for math rigor)
FACT_CHECK_ENABLED = True       # Fact-check each turn
STREAM_OUTPUT = True            # Stream responses in real-time
SAVE_TRANSCRIPT = True          # Save debate transcript
```

---

## Research & Rigor

```python
# Research Synthesis
RESEARCH_MODE = True                    # Generate research kit after debate
RESEARCH_MAX_RECOMMENDATIONS = 5        # Max PhD recommendations

# Academic Rigor
ACADEMIC_RIGOR_MODE = True              # Enforce math backing
THEOREM_EXTRACTION_ENABLED = True       # Extract theorems/proofs
RIGOR_SCORING_ENABLED = True            # Score rigor per turn (0-10)
RESEARCH_GAP_DETECTION_ENABLED = True  # Find PhD-level gaps

# Display Rigor
SHOW_RIGOR_SCORES = True                # Show rigor scores
DETAILED_THEOREM_ANALYSIS = True        # Show theorem details
PhD_RECOMMENDATIONS_ENABLED = True      # Generate PhD advice
```

---

## Phase 5: ICLR Pipeline

### Enable/Disable

```python
GAP_TO_FORMAL_PROBLEM_ENABLED = False   # Convert gaps to formal problems (disabled)
NOVELTY_ANALYZER_ENABLED = False        # Analyze novelty (disabled by default)
SOLUTION_SKETCH_ENABLED = False         # Generate proof sketches (disabled)
ICLR_READINESS_ENABLED = False          # Complete readiness scoring (disabled)
```

### Thresholds

```python
ICLR_NOVELTY_THRESHOLD = 60             # Min novelty to recommend
ICLR_FEASIBILITY_THRESHOLD = 50         # Min feasibility
ICLR_EVIDENCE_QUALITY_THRESHOLD = 0.5   # Min evidence quality (0-1)
ICLR_OVERALL_THRESHOLD = 50             # Min readiness score
```

### Display

```python
SHOW_FORMAL_PROBLEMS = True             # Show formalized problems
SHOW_NOVELTY_ANALYSIS = True            # Show novelty scores
SHOW_SOLUTION_SKETCHES = True           # Show proof strategies
SHOW_ICLR_READINESS = True              # Show readiness scores
SHOW_ACTION_ITEMS = True                # Show action items
```

---

## Phase 7: PhD UX

### Startup Mode

```python
QUICK_START_MODE = True                 # Ask topic only (recommended)
INTERACTIVE_SETUP = True                # Allow inline refinement
```

### Output Style

```python
MINIMAL_OUTPUT = False                  # Skip verbose output
DETAILED_OUTPUT = True                  # Allow detailed output
SHOW_PROGRESS_BARS = True               # Show progress during Phase 5
VERBOSE_LOGGING = False                 # Log to console (not just file)
```

### Feature Toggles

```python
ESTIMATE_API_COST = True                # Show cost before running
SHOW_TOP_GAP_DASHBOARD = True           # Highlight #1 gap
SHOW_STATISTICS_DASHBOARD = True        # Show score averages
ENABLE_BOOKMARKING = True               # Save favorite gaps
ENABLE_RUN_HISTORY = True               # Track past debates
ENABLE_PDF_EXPORT = True                # Export for advisor
ENABLE_ELEVATOR_PITCH = True            # Generate pitches
ENABLE_BATCH_MODE = True                # Run multiple topics
```

### Cost Management

```python
COST_CONFIRMATION_THRESHOLD = 0.50      # Ask before $X cost
FAST_MODE = False                       # Skip optional features
SKIP_RESEARCH_KIT = False               # Skip synthesis
SKIP_RIGOR_SCORING = False              # Skip rigor analysis
SKIP_FACT_CHECK = False                 # Skip fact-checking
```

### Advanced Settings

```python
DEFAULT_NUM_GAPS = 5                    # Default gaps for cost estimation
COST_PER_API_CALL = 0.001              # Cost per call (for estimation)
ELEVATOR_PITCH_SECONDS = 15             # 15, 30, or 60 seconds
DASHBOARD_TOP_N = 3                     # Top N gaps on dashboard
PDF_INCLUDE_TRACE = False               # Include debug logs in PDF
MAX_HISTORY_ENTRIES = 50                # Keep last N debates
```

---

## Caching & Performance

```python
CACHE_PHASE5_RESULTS = True             # Cache API results (60% savings!)
USE_RETRY_CACHE = True                  # Enable LRU cache
CACHE_MAX_SIZE = 500                    # Max cached items
BATCH_SKIP_DUPLICATE_TOPICS = True      # Don't re-run cached topics
```

---

## Display & Output

```python
LANGUAGE = "vi"                         # UI language (vi, en)
LANGUAGE_MIXED_MODE = True              # Vietnamese UI + English technical
COLOR_THEME = "purple"                  # purple, blue, or green
AUTO_SAVE_RESULTS = True                # Auto-save without asking
EXPORT_INCLUDE_DETAILED_ANALYSIS = True # Include full analysis in exports
EXPORT_AUTO_OPEN_HTML = False           # Auto-open HTML in browser
```

---

## File Paths

```python
TRANSCRIPT_DIR = "transcripts"          # Debate transcripts
RESEARCH_KIT_DIR = "research_kits"      # Research kits
PhD_ANALYSIS_DIR = "phd_analysis"       # PhD analysis output

# Phase 7 locations
BOOKMARK_FILE = "phd_analysis/bookmarks.json"
HISTORY_FILE = "phd_analysis/run_history.json"
ADVISOR_EXPORT_DIR = "phd_analysis/advisor_reports"
BATCH_FILE = None                       # CSV with topics (None = ask)
BATCH_RESULTS_DIR = "phd_analysis/batch_results"
CACHE_DIR = "phd_analysis/.cache"       # API cache
```

---

## Recommended Configurations

### 🔥 Maximum Speed

```python
QUICK_START_MODE = True
FAST_MODE = True
SKIP_RESEARCH_KIT = True
NUM_PROFESSORS = 2
MAX_ROUNDS = 1
USE_RETRY_CACHE = True
```

### 💰 Budget Conscious

```python
USE_RETRY_CACHE = True
COST_CONFIRMATION_THRESHOLD = 0.25
FAST_MODE = False  # Still get quality
NUM_PROFESSORS = 2
```

### 🎓 Maximum Quality (Default)

```python
QUICK_START_MODE = True
NUM_PROFESSORS = 3
MAX_ROUNDS = 2
ICLR_READINESS_ENABLED = True
USE_RETRY_CACHE = True
SHOW_TOP_GAP_DASHBOARD = True
```

### 🏃 Development Testing

```python
QUICK_START_MODE = True
NUM_PROFESSORS = 2
MAX_ROUNDS = 1
MAX_TOKENS_PER_TURN = 200
MINIMAL_OUTPUT = True
STREAM_OUTPUT = False
```

---

## 💡 Tips

1. **Always enable caching** (`USE_RETRY_CACHE = True`) — 60% cost savings
2. **Use `QUICK_START_MODE`** — Most use cases need defaults only
3. **Set `COST_CONFIRMATION_THRESHOLD`** — Prevent surprise API costs
4. **Enable `SHOW_TOP_GAP_DASHBOARD`** — See results clearly
5. **Use `FAST_MODE` for preliminary runs** — Then deep dive later

---

## 🐛 Common Issues

### Cost is too high

- Enable: `USE_RETRY_CACHE = True`
- Reduce: `NUM_PROFESSORS = 2`
- Use: `FAST_MODE = True`

### Debates are too long

- Reduce: `MAX_ROUNDS = 1`
- Reduce: `MAX_TOKENS_PER_TURN = 300`
- Use: `FAST_MODE = True`

### Not seeing results

- Set: `SHOW_TOP_GAP_DASHBOARD = True`
- Set: `SHOW_ICLR_READINESS = True`
- Check logs in: `phd_analysis/logs/`

---

**See Also:**

- [Quick Start](../guides/01_QUICK_START.md)
- [Phase 7 Guide](../guides/03_PHASE7_USER_GUIDE.md)
- [Debugging](DEBUGGING.md)
