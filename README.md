<div align="center">

# ⚔️ ProfOcto

**AI-Powered Research Gap Discovery Platform**

_Transform your research brainstorming into ICLR-ready papers through structured academic debate_

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Gemini_API-Free_Tier-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com)
[![React 18+](https://img.shields.io/badge/React-18%2B-61DAFB?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[🚀 Get Started](#quick-start) • [📖 Documentation](#documentation) • [✨ Features](#features) • [🎯 Use Cases](#use-cases)

</div>

---

## 🎯 What is ProfOcto?

ProfOcto helps PhD students and researchers discover novel research gaps by facilitating **structured academic debates** between AI professors. Instead of unstructured brainstorming, you:

1. **Pose a research question** to a panel of diverse AI professors
2. **Watch them debate** with mathematical rigor and counter-arguments
3. **Identify gaps** between different viewpoints
4. **Export insights** as structured research briefs for your advisor

### Why ProfOcto?

- 🧠 **Rigorous debate format** ensures you explore all angles of your research question
- 📊 **Visual gap analysis** reveals unexplored areas in the research landscape
- 💾 **Export capabilities** - generate elevator pitches, PDF reports, research outlines
- ⚡ **Free to use** - powered by Gemini free tier API
- 🌍 **International** - English-first, designed for global research collaboration

---

## ✨ Key Features

### 🎓 Academic Debate Engine

- Multi-professor panel with distinct viewpoints (Empiricist, Theorist, Skeptic, Pragmatist, Historian)
- Automatic moderator summarizing key disagreements
- Web search fact-checking with claim verification

### 📈 Research Gap Discovery

- Automatic identification of contradictions and disagreements
- Structured gap analysis with difficulty levels (Beginner/Master/PhD)
- PhD-ready research recommendations

### 📊 Export & Analysis Tools

- Generate elevator pitches for advisors
- Export debates as Markdown or PDF
- Bookmark important research gaps
- Session history and tracking

### 🎨 Modern UI/UX

- **Web UI**: Real-time streaming debate display, dark mode, responsive design
- **Terminal UI**: Rich formatting with colors, panels, and progress indicators
- **Configuration**: 100+ flags to customize behavior

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Web UI, optional)
- Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

### 1. Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/HZhalex/ProfOcto.git
cd ProfOcto

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key (1 minute)

```bash
# Create .env file
cp .env.example .env

# Edit .env with your Gemini API key
# Get key: https://aistudio.google.com → Get API key → Create API key
```

### 3. Run Terminal UI (5 minutes)

```bash
# Default: interactive mode
python main.py

# Or pass topic directly
python main.py "MoE vs Dense Models" "Distributed Training"
```

### 4. Run Web UI (Optional)

```bash
# Terminal 1 - Backend
uvicorn web.server:app --reload --port 8000

# Terminal 2 - Frontend
cd web
npm run dev

# Open http://localhost:3000
```

---

## 📖 Documentation

### Getting Started

- [**Quick Start Guide**](docs/guides/01_QUICK_START.md) — 5-minute setup walkthrough
- [**Setup Instructions**](docs/guides/02_SETUP.md) — Detailed installation guide
- [**Feature Guide**](docs/guides/03_PHASE7_USER_GUIDE.md) — Complete feature walkthrough

### Features & How They Work

- [**Configuration Reference**](docs/development/CONFIG_REFERENCE.md) — 100+ settable flags explained
- [**Debate System**](docs/features/DEBATE_SYSTEM.md) — How academic debates work
- [**Research Gap Analysis**](docs/features/ACADEMIC_RIGOR.md) — Identifying high-value research directions

### Troubleshooting

- [**Debugging Guide**](docs/development/DEBUGGING.md) — Common issues and solutions
- [**Architecture Overview**](docs/development/ARCHITECTURE.md) — System design details

---

## 🎯 Use Cases

### 👨‍🎓 PhD Students

- **Discover novel research directions** before starting your PhD
- **Validate research ideas** against diverse expert viewpoints
- **Generate talking points** for advisor meetings
- **Create research outlines** for paper drafting

### 🔬 Researchers

- **Explore emerging fields** through structured debate
- **Identify white spaces** in the research landscape
- **Benchmark ideas** against academic consensus
- **Accelerate literature review** with AI-powered analysis

### 📚 Academic Teams

- **Collaborative ideation** - debate together in real-time
- **Export briefs** for team discussions
- **Track historical debates** and insights
- **Build institutional knowledge**

---

## ⚙️ Configuration Examples

### Run with different Gemini models

```python
# In config.py
MODEL = "gemma-3-1b-it"             # Fastest (free tier)
```

### Customize debate structure

```python
NUM_PROFESSORS = 5                  # Panel size (2-5)
MAX_ROUNDS = 3                      # Debate rounds
MAX_TOKENS_PER_TURN = 500           # Response length
FACT_CHECK_ENABLED = True           # Enable/disable fact-checking
```

### Export preferences

```python
SAVE_TRANSCRIPT = True              # Save debate as .md
ENABLE_PDF_EXPORT = True            # Generate PDF reports
ENABLE_BOOKMARKING = True           # Save favorite gaps
```

---

## 🏗️ Project Structure

```
ProfOcto/
├── main.py                    # Entry point - Terminal UI
├── config.py                  # System configuration
├── orchestrator.py            # Generate professors & opening question
│
├── agents/                    # AI Agent modules
│   ├── professor.py           # Debate participant
│   ├── moderator.py           # Debate summaries
│   └── fact_checker.py        # Claim verification
│
├── debate/                    # Debate engine
│   ├── session.py             # Session state management
│   └── turn_manager.py        # Speaking order & flow
│
├── output/                    # Export modules
│   ├── terminal_renderer.py   # Terminal UI with Rich
│   └── exporter.py            # PDF/Markdown export
│
├── prompts/                   # System prompts
│   ├── professor_base.txt
│   └── moderator.txt
│
├── web/                       # Web UI (React + FastAPI)
│   ├── server.py              # Backend API
│   └── src/                   # React components
│
└── docs/                      # Documentation
    ├── guides/                # User guides
    ├── features/              # Feature documentation
    └── development/           # Dev & config reference
```

---

## 📊 Performance & Costs

| Model                | Free Tier     | Quality    | Speed  | Cost/Month |
| -------------------- | ------------- | ---------- | ------ | ---------- |
| **Gemma 3.1B**       | ✅ 30 req     | ⭐⭐       | ⚡⚡⚡ | Free       |

### Estimated costs for a typical debate:

- **Model**: Gemma 3.1B (recommended)
- **Topic complexity**: Medium (5 professors, 2 rounds)
- **Cost per debate**: ~$0.01-0.05 USD
- **100 debates/month**: <$5 USD

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes and test thoroughly
4. Submit a pull request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black . && isort .
```

---

## 🐛 Troubleshooting

### API Key Issues

**Problem**: "GEMINI_API_KEY not found"  
**Solution**: Create `.env` file with your API key from [aistudio.google.com](https://aistudio.google.com)

### Rate Limiting

**Problem**: "429 Too Many Requests"  
**Solution**: Switch to a model with higher free tier limits or add a 1-2 second delay between requests

### Web UI Not Loading

**Problem**: Frontend shows blank page  
**Solution**:

```bash
# Restart backend
.venv\Scripts\activate
uvicorn web.server:app --reload --port 8000

# In another terminal, restart frontend
cd web && npm run dev
```

### Debate Quality Issues

**Problem**: Professors responding with generic answers  
**Solution**:

- Use a stronger model (Gemma 3.1B)
- Make topic more specific
- Increase `MAX_TOKENS_PER_TURN` in config

---

## 📚 Learning Resources

- [Prompts Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Academic Writing Best Practices](https://www.citefactor.org/)
- [Research Gap Analysis Methods](https://www.jstor.org/)
- [Gemini API Documentation](https://ai.google.dev)

---

## 📄 License

MIT License - Free for personal, educational, and commercial use. See [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev)
- UI powered by [React](https://react.dev) and [Rich](https://rich.readthedocs.io)
- Database management with [SQLite](https://www.sqlite.org/)

---

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
