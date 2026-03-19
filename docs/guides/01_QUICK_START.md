# Quick Start Guide

Get ProfOcto running and analyze your first research gap in under 5 minutes.

---

## Prerequisites

- **Python 3.10+**
- **Gemini API key** — free from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 1. Setup

```bash
cd ProfOcto

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
cp .env.example .env
# Edit .env and paste your key: GEMINI_API_KEY=AIza...
```

## 2. Run Your First Analysis

```bash
python main.py
```

You'll be prompted for one thing:

```
What research topic or problem would you like to explore?
> [Type your research question]
```

ProfOcto then runs automatically:

1. Generates a panel of AI professors with distinct viewpoints
2. Runs a structured debate on your topic
3. Fact-checks claims via web search
4. Extracts theorems, scores rigor, identifies research gaps
5. Displays a dashboard with research gap recommendations
6. Offers interactive options (bookmark, export, elevator pitch)

## 3. What You'll See

### Cost Estimate (shown before execution)

```
Cost & Timeline Estimate
  Estimated API Cost: $0.87
  Estimated Runtime: 2.7m
  Cache Status: Enabled (60% cost reduction)
```

### Top Gap Dashboard (shown after analysis)

```
╔════════════════════════════════════════════╗
║ TOP GAP #1 (RECOMMENDED FOR PURSUIT)       ║
║ Readiness: 85/100                         ║
║ Novelty: 80/100 | Feasibility: 85/100     ║
║ Timeline: ~6 months                       ║
╚════════════════════════════════════════════╝
```

### Interactive Menu

After analysis completes, you can:

- **Bookmark** a gap for later review
- **Export** gap analysis as a report for your advisor
- **Generate** an elevator pitch (15/30/60 seconds)
- **Compare** with previous debate sessions

## 4. Output Files

After a run, your results are saved to:

```
transcripts/                    # Debate transcript (Markdown)
research_kits/                  # Research kit (JSON)
logs/                           # Detailed session logs
phd_analysis/
├── bookmarks.json             # Bookmarked gaps
├── run_history.json           # Past sessions
├── advisor_reports/           # Exported reports
└── .cache/                    # API cache (~60% cost savings)
```

## 5. CLI Arguments (Optional)

You can skip the interactive prompt by passing topic and field directly:

```bash
python main.py "MoE vs Dense Models" "Distributed Training"
```

## 6. Customization (Optional)

Before a run, you can optionally refine settings:

```
Customize settings before running? [y/N]: y

Options:
  [1] Change topic
  [2] Change field
  [3] Toggle Phase 5 analysis
  [5] Skip optional features (fast mode)
```

Or edit `config.py` directly. See [Configuration Reference](../development/CONFIG_REFERENCE.md) for all flags.

---

## Speed Tips

- **Fast mode**: Set `FAST_MODE = True` in `config.py` — skips optional features, reduces runtime by ~30–40%
- **Budget control**: Set `COST_CONFIRMATION_THRESHOLD = 0.25` — asks before spending more than $0.25

---

## Troubleshooting

### "API key error"

- Verify `.env` exists in the project root with the correct key
- Regenerate your key at [Google AI Studio](https://aistudio.google.com/app/apikey)

### "429 Too Many Requests"

- Free tier limit: 15 requests/minute. Wait a minute and try again
- Reduce `NUM_PROFESSORS` in `config.py`

### Dashboard not showing

- Ensure `SHOW_TOP_GAP_DASHBOARD = True` in `config.py`
- Ensure `RESEARCH_GAP_DETECTION_ENABLED = True`

---

## Next Steps

- [Setup & Installation](02_SETUP.md) — Detailed environment setup
- [Feature Guide](03_PHASE7_USER_GUIDE.md) — Complete walkthrough of all features
- [Configuration Reference](../development/CONFIG_REFERENCE.md) — All 100+ config flags
