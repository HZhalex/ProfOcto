<div align="center">

# ProfOcto

**AI-Powered Research Gap Discovery Through Structured Academic Debate**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Gemini_API-Free_Tier-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![React 18+](https://img.shields.io/badge/React-18%2B-61DAFB?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Get Started](#-quick-start) · [Documentation](#-documentation) · [Features](#-features) · [Use Cases](#-use-cases)

</div>

---

## What is ProfOcto?

ProfOcto orchestrates **structured academic debates** between AI-generated professors to help PhD students and researchers discover novel research gaps. Each professor has a distinct role (Empiricist, Theorist, Skeptic, Pragmatist, Historian), a realistic academic affiliation, and a specific methodological stance.

**How it works:**

1. You provide a **research topic** and field (e.g., "MoE vs Dense Models" in "Distributed Training")
2. ProfOcto generates a panel of AI professors with diverse viewpoints
3. The professors **debate** with mathematical rigor, citing theorems and proofs
4. A moderator summarizes key disagreements after each round
5. The system **identifies research gaps** from contradictions and trade-offs in the debate
6. Optionally, an **ICLR readiness pipeline** scores each gap for novelty, feasibility, and publication readiness

**Powered by**: Google Gemini API (free tier) — default model: `gemma-3-1b-it`

---

## Features

### Academic Debate Engine

- **Multi-professor panel** (2–5 professors) with distinct roles and stances
- **Fact-checking** with web search verification on each turn
- **Theorem extraction** — automatically identifies theorems, lemmas, proofs, and citations
- **Rigor scoring** — rates each turn on mathematical backing (0–10 scale)
- **Moderator summaries** after each round highlighting key disagreements
- **Real-time streaming** of professor responses

### Research Gap Discovery

- Automatic detection of **contradictions**, **assumption violations**, and **efficiency-quality trade-offs**
- Gaps tagged by difficulty level (Beginner / Master / PhD)
- PhD-ready research recommendations

### ICLR Readiness Pipeline (Phase 5)

When enabled, processes each gap through four stages:

1. **Gap Formalization** — converts informal gaps into formal mathematical problem statements
2. **Novelty Analysis** — scores novelty vs. state-of-the-art (0–100)
3. **Solution Sketch** — generates proof strategies and methodological approaches
4. **Readiness Assessment** — combines novelty, feasibility, and evidence quality into a final score

### PhD-Friendly UX (Phase 7)

- **Quick Start Mode** — just enter your topic, everything else uses sensible defaults
- **Cost & Runtime Estimator** — shows projected API cost and runtime before execution
- **Top Gap Dashboard** — prominently displays the #1 recommended gap with scores
- **Bookmarking** — save gaps for long-term research planning
- **Elevator Pitch Generator** — 15/30/60-second verbal summaries for advisor meetings
- **Advisor Export** — export gap analyses as TXT, HTML, or JSON reports
- **Batch Mode** — process multiple topics from a CSV file
- **Run History** — track and compare past debate sessions

### Dual Interface

- **Web UI** — React 18 frontend with real-time SSE streaming, dark mode, topic library, and debate history
- **Terminal UI** — Rich-formatted output with colored panels, tables, and progress indicators

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** (only for Web UI — optional)
- **Gemini API key** — free at [aistudio.google.com](https://aistudio.google.com/app/apikey)

### 1. Install

```bash
git clone https://github.com/HZhalex/ProfOcto.git
cd ProfOcto

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Install dependencies (only 4 packages)
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and paste your Gemini API key:
# GEMINI_API_KEY=AIza...
```

### 3. Run (Terminal)

```bash
# Interactive mode — prompts for topic
python main.py

# Direct mode — pass topic and field as arguments
python main.py "MoE vs Dense Models" "Distributed Training"
```

### 4. Run (Web UI — Optional)

```bash
# Terminal 1: Start FastAPI backend
uvicorn web.server:app --reload --port 8000

# Terminal 2: Start React dev server
cd web
npm install   # first time only
npm run dev

# Open http://127.0.0.1:3000/
```

For production, run `npm run build` inside `web/` — FastAPI will serve the built frontend from `web/dist/`.

---

## Documentation

| Guide                                                           | Description                          |
| --------------------------------------------------------------- | ------------------------------------ |
| [Quick Start](docs/guides/01_QUICK_START.md)                    | Get running in 5 minutes             |
| [Setup & Installation](docs/guides/02_SETUP.md)                 | Detailed environment setup           |
| [Feature Guide](docs/guides/03_PHASE7_USER_GUIDE.md)            | Complete walkthrough of all features |
| [Configuration Reference](docs/development/CONFIG_REFERENCE.md) | All 100+ config flags explained      |
| [Web UI Guide](web/README_WEB.md)                               | Web interface setup and usage        |

---

## Use Cases

### PhD Students

- Discover novel research directions before committing to a topic
- Validate ideas against diverse expert viewpoints
- Generate elevator pitches and talking points for advisor meetings
- Export structured research briefs for proposals

### Researchers

- Explore emerging fields through structured multi-perspective debate
- Identify white spaces in the research landscape
- Accelerate literature review with AI-powered gap analysis

### Academic Teams

- Run batch analyses across multiple research questions
- Track debate history to find robust, recurring gaps
- Share professional exports with committee members

---

## Configuration Highlights

All configuration is in `config.py`. Key settings:

```python
# AI Model (default: gemma-3-1b-it, free tier)
MODEL = "gemma-3-1b-it"

# Debate structure
NUM_PROFESSORS = 2              # Panel size (2–5)
MAX_ROUNDS = 1                  # Debate rounds
MAX_TOKENS_PER_TURN = 700       # Max tokens per response
FACT_CHECK_ENABLED = True       # Fact-check each turn

# Research analysis
RESEARCH_MODE = True            # Generate research kit after debate
ACADEMIC_RIGOR_MODE = True      # Enforce mathematical backing
THEOREM_EXTRACTION_ENABLED = True
RIGOR_SCORING_ENABLED = True
RESEARCH_GAP_DETECTION_ENABLED = True

# ICLR Pipeline (disabled by default — resource intensive)
GAP_TO_FORMAL_PROBLEM_ENABLED = False
NOVELTY_ANALYZER_ENABLED = False
SOLUTION_SKETCH_ENABLED = False
ICLR_READINESS_ENABLED = False

# PhD UX features (all enabled by default)
QUICK_START_MODE = True
ESTIMATE_API_COST = True
SHOW_TOP_GAP_DASHBOARD = True
ENABLE_BOOKMARKING = True
ENABLE_ELEVATOR_PITCH = True
ENABLE_PDF_EXPORT = True
ENABLE_BATCH_MODE = True

# Caching (enabled by default — ~60% cost savings)
USE_RETRY_CACHE = True
CACHE_PHASE5_RESULTS = True
```

See [Configuration Reference](docs/development/CONFIG_REFERENCE.md) for all 100+ flags.

---

## Project Structure

```
ProfOcto/
├── main.py                         # Entry point (Terminal UI)
├── config.py                       # 100+ configuration flags
├── orchestrator.py                 # Professor generation & debate setup
├── requirements.txt                # Dependencies (4 packages)
├── .env.example                    # Environment variable template
│
├── agents/                         # 13 AI analysis agents
│   ├── professor.py                #   Generate professor debate responses
│   ├── moderator.py                #   Moderator summaries & openings
│   ├── fact_checker.py             #   Web search fact verification
│   ├── research_synthesizer.py     #   Research kit & paper outline generation
│   ├── theorem_extractor.py        #   Extract theorems, lemmas, proofs
│   ├── rigor_scorer.py             #   Mathematical rigor scoring (0–10)
│   ├── gap_identifier.py           #   Identify research gaps from debate
│   ├── gap_ranker.py               #   Rank gaps by novelty/feasibility/impact
│   ├── gap_to_formal_problem.py    #   Convert gaps to formal problem statements
│   ├── novelty_analyzer.py         #   Score novelty vs SOTA (0–100)
│   ├── solution_sketch.py          #   Generate proof strategies
│   ├── iclr_readiness_scorer.py    #   ICLR publication readiness assessment
│   └── academic_validator.py       #   Citation extraction & claim verification
│
├── debate/                         # Debate engine
│   ├── session.py                  #   Session state, Turn, ProfessorProfile
│   └── turn_manager.py             #   Round-robin order & repetition detection
│
├── output/                         # Output & export modules
│   ├── terminal_renderer.py        #   Rich terminal formatting
│   ├── exporter.py                 #   Markdown transcript export
│   ├── phase5_exporter.py          #   ICLR analysis export (JSON + HTML)
│   ├── interactive_cli.py          #   Interactive gap exploration menu
│   ├── phd_startup_cli.py          #   Quick/interactive startup flow
│   ├── cost_estimator.py           #   API cost & runtime estimation
│   ├── gap_dashboard.py            #   Top gap dashboard display
│   ├── elevator_pitch.py           #   Verbal summary generator
│   ├── pdf_exporter.py             #   Advisor report export (TXT/HTML/JSON)
│   └── batch_processor.py          #   Multi-topic batch processing
│
├── prompts/                        # System prompts for AI agents
│   ├── professor_base.txt          #   Core professor personality
│   ├── moderator.txt               #   Moderator role definition
│   ├── fact_checker.txt            #   Fact-checker instructions
│   ├── system/                     #   Advanced professor & moderator prompts
│   ├── research/                   #   Research synthesis prompts
│   └── templates/                  #   Turn & output formatting templates
│
├── utils/                          # Utilities
│   ├── logger.py                   #   Centralized logging (5 log files)
│   ├── bookmark_history.py         #   Bookmark & run history managers
│   └── retry_cache.py             #   LRU API cache with disk persistence
│
├── web/                            # Web UI
│   ├── server.py                   #   FastAPI backend with SSE streaming
│   └── src/                        #   React 18 frontend
│
├── docs/                           # Documentation
│   ├── guides/                     #   User guides (quick start, setup, features)
│   └── development/                #   Configuration reference
│
├── transcripts/                    # Saved debate transcripts
├── research_kits/                  # Generated research kits
└── logs/                           # Session & debug logs
```

---

## Dependencies

ProfOcto has a minimal dependency footprint:

| Package        | Version | Purpose                                      |
| -------------- | ------- | -------------------------------------------- |
| `google-genai` | 1.10.0  | Gemini API client                            |
| `rich`         | 13.9.4  | Terminal formatting (tables, panels, colors) |
| `fastapi`      | 0.115.0 | Web API framework                            |
| `uvicorn`      | 0.30.6  | ASGI server for FastAPI                      |

---

## Troubleshooting

### "GEMINI_API_KEY not found"

Create a `.env` file in the project root with your API key:

```
GEMINI_API_KEY=AIza...
```

Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

### "429 Too Many Requests"

The free tier has rate limits (15 requests/minute). Reduce `NUM_PROFESSORS` or `MAX_ROUNDS` in `config.py`, or wait a minute between runs.

### Web UI shows blank page

Make sure both the backend and frontend are running:

```bash
# Terminal 1: Backend
uvicorn web.server:app --reload --port 8000

# Terminal 2: Frontend
cd web && npm install && npm run dev
```

### Low-quality debate responses

- Make your topic more specific (e.g., "MoE routing strategies for long-context LLMs" instead of "LLMs")
- Increase `MAX_TOKENS_PER_TURN` in `config.py`

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Submit a pull request

---

## License

MIT License — free for personal, educational, and commercial use. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Google Gemini API](https://ai.google.dev) — LLM backend
- [Rich](https://rich.readthedocs.io) — Terminal UI framework
- [React](https://react.dev) — Web frontend framework
- [FastAPI](https://fastapi.tiangolo.com) — Web API framework

## 💡 Roadmap

- [ ] Multi-language support (Vietnamese, Mandarin, Spanish)
- [ ] Advanced debate modes (moderated adversarial, Socratic method)
- [ ] Research paper auto-generation pipeline
- [ ] Integration with academic databases (arXiv, Scholar)
- [ ] Team collaboration features with real-time syncing
- [ ] Mobile app for iOS/Android

---

<div align="center">

**Have a question?** [Start a Discussion](https://github.com/HZhalex/ProfOcto/discussions)  
**Found a bug?** [Report an Issue](https://github.com/HZhalex/ProfOcto/issues)

Made with ❤️ for the research community

</div>
