# Feature Guide

Complete walkthrough of all ProfOcto features. This covers the debate engine, research analysis, ICLR readiness pipeline, and PhD-friendly UX features.

---

## Table of Contents

- [Quick Start Mode](#quick-start-mode)
- [Cost & Timeline Estimator](#cost--timeline-estimator)
- [Top Gap Dashboard](#top-gap-dashboard)
- [Bookmarking](#bookmarking)
- [Elevator Pitch Generator](#elevator-pitch-generator)
- [Advisor Export](#advisor-export)
- [Run History & Comparison](#run-history--comparison)
- [Batch Mode](#batch-mode)
- [Configuration Quick Reference](#configuration-quick-reference)
- [Typical PhD Workflow](#typical-phd-workflow)
- [Troubleshooting](#troubleshooting)

---

## Quick Start Mode

**What it does:** Reduces startup to a single question — your research topic. All other settings use defaults.

**Before:** 5–10 setup questions every run.  
**After:** One prompt, then automatic execution.

### Usage

```bash
python main.py
```

```
What research topic or problem would you like to explore?
> [Your question here]

Estimated Cost & Timeline:
  API Cost: $0.87
  Runtime: 2.7m

Run advanced ICLR readiness analysis? [Y/n]: y

Customize settings before running? [y/N]: n
```

If you choose to customize, you can adjust settings inline:

```
Options:
  [1] Change topic
  [2] Change field
  [3] Toggle Phase 5 analysis
  [5] Skip optional features (fast mode)
```

### Configuration

```python
QUICK_START_MODE = True         # Enable one-question startup
INTERACTIVE_SETUP = True        # Allow inline refinement
```

---

## Cost & Timeline Estimator

**What it does:** Shows the projected API cost and runtime **before** execution begins, so you can decide whether to proceed.

### Output Example

```
Cost & Timeline Estimate
──────────────────────────────────────────

Gaps to Process: 5
Estimated API Cost: $0.87
Estimated Runtime: 2.7m

Cost Breakdown:
  Gap Formalization: $0.20
  Novelty Analysis: $0.15
  Solution Sketching: $0.27
  Readiness Scoring: $0.25

Cache Status: Enabled (60% cost reduction)
```

If the estimated cost exceeds the confirmation threshold, ProfOcto asks for confirmation before proceeding.

### Configuration

```python
ESTIMATE_API_COST = True                # Show cost estimate
COST_CONFIRMATION_THRESHOLD = 0.50      # Confirm if cost > $0.50
ESTIMATE_RUNTIME = True                 # Show runtime estimate
COST_PER_API_CALL = 0.001              # Estimated cost per API call (USD)
USE_RETRY_CACHE = True                  # ~60% cost savings via caching
FAST_MODE = False                       # Skip optional features to save cost
```

---

## Top Gap Dashboard

**What it does:** After analysis completes, prominently displays the #1 recommended research gap with all scores.

### Display

```
╔════════════════════════════════════════════════════╗
║ TOP GAP #1 (RECOMMENDED FOR PURSUIT)               ║
╠════════════════════════════════════════════════════╣
║ Novel transformer efficiency optimization          ║
║ via low-rank approximation                         ║
╠════════════════════════════════════════════════════╣
║ Status: HIGHLY READY                              ║
║ Readiness Score: 85/100                           ║
║ Novelty: 80/100 | Feasibility: 85/100             ║
║ Timeline: ~6 months                               ║
╠════════════════════════════════════════════════════╣
║ Recommendation: Strong novelty + high              ║
║ feasibility = ICLR-competitive. Start with         ║
║ literature review.                                 ║
╚════════════════════════════════════════════════════╝
```

The statistics view also shows averages across all identified gaps:

- Average readiness score
- Average novelty score
- Average feasibility score

### Configuration

```python
SHOW_TOP_GAP_DASHBOARD = True       # Enable dashboard display
SHOW_STATISTICS_DASHBOARD = True    # Show averages
DASHBOARD_TOP_N = 3                 # Number of top gaps to show
DASHBOARD_MINIMAL_VIEW = False      # Compact layout
```

---

## Bookmarking

**What it does:** Save research gaps for later reference — useful for long-term topic selection across multiple sessions.

### Usage

From the interactive menu after a debate:

```
[2] Bookmark your favorite gap

Which gap to bookmark? (1-5 or 0 for top): 1
Optional notes: "Verify against latest ICML 2025 papers"

Gap bookmarked!
```

### Features

- View all bookmarked gaps with scores
- Add or update personal notes on each bookmark
- Remove bookmarks
- Bookmarks persist across sessions

### Storage

Saved to: `phd_analysis/bookmarks.json`

### Configuration

```python
ENABLE_BOOKMARKING = True
BOOKMARK_FILE = "phd_analysis/bookmarks.json"
```

---

## Elevator Pitch Generator

**What it does:** Generates a concise verbal summary of a research gap, suitable for advisor meetings, lab presentations, or interview explanations.

### Usage

From the interactive menu:

```
[4] Generate elevator pitch

Which gap? (1-5): 2

Elevator Pitch (30 sec):

This research gap addresses transformer efficiency limitations.
By tackling this novel opportunity, we can advance the field in
3-6 months. The innovation lies in developing low-rank methods
combined with dynamic compression.

Key Points:
  Gap: Novel low-rank transformer approximation
  Novelty Score: 80/100
  Innovation Level: Significant
  Timeline: 6 months realistic
  Readiness: 85/100 ICLR-ready
```

### Duration Options

| Duration   | Use Case                                  |
| ---------- | ----------------------------------------- |
| 15 seconds | Quick hook for hallway conversations      |
| 30 seconds | Standard pitch for office hours (default) |
| 60 seconds | Extended pitch with motivation and impact |

### Configuration

```python
ENABLE_ELEVATOR_PITCH = True
ELEVATOR_PITCH_SECONDS = 15         # Default: 15, 30, or 60
```

---

## Advisor Export

**What it does:** Exports a gap analysis as a professional report for sharing with your advisor or committee members.

### Usage

From the interactive menu:

```
[3] Export gap analysis for advisor

Which gap to export? (1-5 or 'all'): 1

Exported to: phd_analysis/advisor_reports/
  Novel_transformer_20260317_120000.txt
```

### Report Contents

- Gap title and readiness score
- Formal problem statement
- Key innovations
- Timeline breakdown (literature review, formalization, development, experimentation, writing)
- Key risks and mitigation strategies
- Next steps
- Required resources

### Export Formats

| Format  | Best For                                  |
| ------- | ----------------------------------------- |
| `.txt`  | Email attachments, simple sharing         |
| `.html` | Browser viewing, formatted reports        |
| `.json` | Programmatic processing, data integration |

### Configuration

```python
ENABLE_PDF_EXPORT = True
ADVISOR_EXPORT_DIR = "phd_analysis/advisor_reports"
PDF_INCLUDE_TRACE = False               # Include debug logs in export
```

---

## Run History & Comparison

**What it does:** Tracks all debate sessions so you can compare results across runs and identify gaps that persist across different topic formulations.

### Usage

From the interactive menu:

```
[5] Compare with previous runs

Recent Debates:
  1. Transformer efficiency (2026-03-17)
  2. MoE scaling strategies (2026-03-16)
  3. Attention mechanisms (2026-03-15)
```

### What's Tracked

- Topic analyzed
- Date and time
- Number of gaps found
- Top gaps with scores
- Full gap details

### Why This Matters

- **Robust gaps** = gaps that appear across multiple analyses are more likely publishable
- **Score trends** = see how your gap identification improves over time
- **Patterns** = understand your research interests from history

### Configuration

```python
ENABLE_RUN_HISTORY = True
HISTORY_FILE = "phd_analysis/run_history.json"
MAX_HISTORY_ENTRIES = 50
```

---

## Batch Mode

**What it does:** Process multiple research questions in sequence from a CSV file. Useful for comparing the same topic from different angles or exploring a set of related questions.

### Setup

Create a CSV file:

```csv
topic,field
"How to improve transformer efficiency?","NLP"
"MoE scaling strategies","Distributed Systems"
"Attention optimization","Computer Vision"
```

### Usage

```python
# In config.py:
ENABLE_BATCH_MODE = True
BATCH_FILE = "batch.csv"
```

```bash
python main.py
```

### Output

```
Processing 1/3: Transformer efficiency...
Processing 2/3: MoE scaling...
Processing 3/3: Attention optimization...

Batch Summary:
  Total gaps found: 15
  Recurring gaps: 3
  Average readiness: 72/100
```

Results saved to `phd_analysis/batch_results/`.

### Configuration

```python
ENABLE_BATCH_MODE = True
BATCH_FILE = None                               # Path to CSV, or None to prompt
BATCH_RESULTS_DIR = "phd_analysis/batch_results"
BATCH_SKIP_DUPLICATE_TOPICS = True              # Skip already-processed topics
```

---

## Configuration Quick Reference

### Startup

```python
QUICK_START_MODE = True
INTERACTIVE_SETUP = True
```

### Display

```python
MINIMAL_OUTPUT = False
DETAILED_OUTPUT = True
SHOW_TOP_GAP_DASHBOARD = True
SHOW_STATISTICS_DASHBOARD = True
```

### Cost

```python
ESTIMATE_API_COST = True
COST_CONFIRMATION_THRESHOLD = 0.50
USE_RETRY_CACHE = True
FAST_MODE = False
```

### Features

```python
ENABLE_BOOKMARKING = True
ENABLE_RUN_HISTORY = True
ENABLE_PDF_EXPORT = True
ENABLE_ELEVATOR_PITCH = True
ENABLE_BATCH_MODE = True
```

### File Paths

```python
BOOKMARK_FILE = "phd_analysis/bookmarks.json"
HISTORY_FILE = "phd_analysis/run_history.json"
ADVISOR_EXPORT_DIR = "phd_analysis/advisor_reports"
BATCH_FILE = None
BATCH_RESULTS_DIR = "phd_analysis/batch_results"
```

See [Configuration Reference](../development/CONFIG_REFERENCE.md) for the complete list.

---

## Typical PhD Workflow

### Day 1: Explore

```bash
python main.py
# Enter your research topic → review cost → run → see top gap dashboard

# Bookmark the best gap:
[2] Bookmark this gap
# Notes: "Start literature review next week"
```

### Day 2: Advisor Meeting

```
# Export a report:
[3] Export for advisor

# Prepare a verbal summary:
[4] Generate elevator pitch
```

### Week 1: Multi-Angle Research

```bash
# Run 3 formulations of the same question
python main.py "Transformer efficiency" "NLP"
python main.py "Low-rank model compression" "ML Systems"
python main.py "Efficient attention mechanisms" "Computer Vision"

# Compare results:
[5] Compare with previous runs
# Gaps appearing in multiple runs → robust research directions
```

---

## Troubleshooting

### Cost is too high

- Caching is on by default (`USE_RETRY_CACHE = True`)
- Enable fast mode: `FAST_MODE = True`
- Reduce panel: `NUM_PROFESSORS = 2`
- Disable Phase 5: all four `*_ENABLED` flags = `False` (default)

### Dashboard not showing

- Ensure `SHOW_TOP_GAP_DASHBOARD = True`
- Ensure `RESEARCH_GAP_DETECTION_ENABLED = True`
- At least 2 gaps must be identified

### Bookmarks not saving

- Check write permissions on `phd_analysis/` directory
- Verify `BOOKMARK_FILE` path in `config.py`

### Export files missing

- Ensure `ENABLE_PDF_EXPORT = True`
- Check that `phd_analysis/advisor_reports/` exists or can be created
- Reports are saved as `.txt` / `.html` / `.json` (not actual PDF)

---

**See also:**

- [Quick Start](01_QUICK_START.md) — 5-minute setup
- [Setup & Installation](02_SETUP.md) — Detailed environment setup
- [Configuration Reference](../development/CONFIG_REFERENCE.md) — All 100+ flags
