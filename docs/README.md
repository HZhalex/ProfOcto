# ProfOcto Documentation

Welcome to the ProfOcto documentation — an AI-powered research gap discovery platform for PhD students and researchers.

---

## Guides

| Guide                                           | Description                                                                      |
| ----------------------------------------------- | -------------------------------------------------------------------------------- |
| [Quick Start](guides/01_QUICK_START.md)         | Get running and analyze your first research gap in 5 minutes                     |
| [Setup & Installation](guides/02_SETUP.md)      | Detailed environment setup, API key configuration, and verification              |
| [Feature Guide](guides/03_PHASE7_USER_GUIDE.md) | Complete walkthrough of all features: dashboard, bookmarking, export, batch mode |

## Reference

| Reference                                                  | Description                                                 |
| ---------------------------------------------------------- | ----------------------------------------------------------- |
| [Configuration Reference](development/CONFIG_REFERENCE.md) | All 100+ configuration flags with descriptions and defaults |

## Web UI

| Guide                                | Description                                      |
| ------------------------------------ | ------------------------------------------------ |
| [Web UI Setup](../web/README_WEB.md) | React frontend + FastAPI backend setup and usage |

---

## Where to Start

**New user?** Start with the [Quick Start Guide](guides/01_QUICK_START.md) — you'll have your first research gap analysis running in 5 minutes.

**Want to customize behavior?** See the [Configuration Reference](development/CONFIG_REFERENCE.md) for all available flags.

**Want the web interface?** See the [Web UI Setup](../web/README_WEB.md) guide.

---

## How ProfOcto Works

ProfOcto runs a multi-phase pipeline:

### Phase 1–4: Debate & Analysis

1. **Professor Generation** — Creates a panel of 2–5 AI professors with distinct roles (Empiricist, Theorist, Skeptic, Pragmatist, Historian) and realistic academic affiliations
2. **Structured Debate** — Professors debate your topic across multiple rounds, enforcing mathematical rigor with theorem citations and proofs
3. **Fact-Checking** — Each turn is verified using web search
4. **Research Synthesis** — Generates a research kit with findings, paper outline, and recommendations

### Phase 5: ICLR Readiness Pipeline (Optional)

When enabled, each identified gap goes through:

1. **Gap Formalization** — Converts informal gaps to formal mathematical problem statements
2. **Novelty Analysis** — Scores novelty vs. state-of-the-art (0–100)
3. **Solution Sketch** — Generates proof strategies and methodological approaches
4. **Readiness Assessment** — Combines all scores into an overall ICLR readiness rating

### Phase 7: PhD-Friendly UX

Interactive features for PhD workflow:

- **Quick Start** — Just enter your topic
- **Cost Estimator** — See projected cost and runtime before execution
- **Top Gap Dashboard** — See the #1 recommended gap prominently displayed
- **Bookmarking** — Save gaps for later
- **Elevator Pitch** — Generate verbal summaries for advisor meetings
- **Advisor Export** — Professional reports in TXT/HTML/JSON
- **Batch Mode** — Process multiple topics from CSV
- **Run History** — Track and compare past sessions

---

## Key Concepts

| Term                     | Definition                                                                      |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Research Gap**         | An unsolved problem in academic literature, suitable for PhD research           |
| **ICLR Readiness Score** | 0–100 score indicating publication readiness at top-tier venues                 |
| **Novelty Score**        | How novel a gap is compared to existing state-of-the-art                        |
| **Feasibility Score**    | How realistic the gap is to solve within a PhD timeline                         |
| **Rigor Score**          | 0–10 rating of mathematical backing in a debate turn                            |
| **Elevator Pitch**       | A 15–60 second verbal summary for presentations                                 |
| **Research Kit**         | Structured output containing findings, gaps, recommendations, and paper outline |

---

## Configuration Overview

All configuration is centralized in `config.py`. Key areas:

- **AI Model** — Default: `gemma-3-1b-it` (Gemini free tier)
- **Debate Structure** — Number of professors, rounds, tokens per turn
- **Research Analysis** — Theorem extraction, rigor scoring, gap detection
- **ICLR Pipeline** — Formalization, novelty, solution sketches, readiness (disabled by default)
- **PhD UX** — Quick start, cost estimation, dashboard, bookmarking, export
- **Caching** — API result caching for ~60% cost savings

See [Configuration Reference](development/CONFIG_REFERENCE.md) for the complete list.

---

## Output Files

After running ProfOcto, output is saved to:

```
transcripts/              # Debate transcripts (Markdown)
research_kits/            # Research kits (JSON)
logs/                     # Session, theorem, rigor, gap, and error logs
phd_analysis/             # PhD analysis output (when ICLR pipeline is enabled)
├── bookmarks.json        #   Saved research gaps
├── run_history.json      #   Past debate sessions
├── advisor_reports/      #   Exported reports for advisor
├── batch_results/        #   Batch processing output
└── .cache/               #   API result cache
```
