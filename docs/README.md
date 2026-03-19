# 📚 ProfOcto Documentation

Welcome to ProfOcto - AI-Powered Research Gap Discovery for PhD Students.

## 📖 Quick Navigation

### 🚀 Getting Started

- **[Quick Start Guide](guides/01_QUICK_START.md)** — Run your first analysis in 5 minutes
- **[Installation & Setup](guides/02_SETUP.md)** — Configure environment variables

### 🎓 Features

#### Phase 7: PhD-Friendly UX (LATEST)

- **[Phase 7 User Guide](guides/03_PHASE7_USER_GUIDE.md)** — All 7 new features explained
  - Quick/Interactive startup
  - Cost estimation
  - Gap dashboard
  - Bookmarking system
  - Elevator pitch generator
  - PDF export for advisor
  - Batch processing

#### Phase 5: ICLR Readiness Pipeline

- **[Phase 5 Implementation](features/PHASE5_ICLR_PIPELINE.md)** — Formalize → Novelty → Sketch → Readiness
- **[Academic Rigor System](features/ACADEMIC_RIGOR.md)** — Mathematical rigor scoring

#### Phase 1-4: Core Debate Engine

- **[Research Mode Guide](features/RESEARCH_MODE.md)** — Automatic paper outline generation
- **[Debate System](features/DEBATE_SYSTEM.md)** — Multi-professor discussion engine

### 🛠️ Development & Configuration

- **[Configuration Reference](development/CONFIG_REFERENCE.md)** — All 100+ config flags explained
- **[Debugging Guide](development/DEBUGGING.md)** — Troubleshooting and logs

### 📋 Project Status

- **[Phase 7 Completion Report](features/PHASE7_COMPLETION_REPORT.md)** — Implementation details, test results
- **[Test Reports](development/TESTING.md)** — Validation results

---

## 🎯 Choose Your Starting Point

**I'm a PhD student ready to start:**
→ Go to [Quick Start Guide](guides/01_QUICK_START.md)

**I want to understand all features:**
→ Go to [Phase 7 User Guide](guides/03_PHASE7_USER_GUIDE.md)

**I need to configure something:**
→ Go to [Config Reference](development/CONFIG_REFERENCE.md)

**I'm having issues:**
→ Go to [Debugging Guide](development/DEBUGGING.md)

**I want to contribute/understand codebase:**
→ Go to [Architecture & Development](development/ARCHITECTURE.md)

---

## 🗂️ Directory Structure

```
docs/
├── guides/                 # User guides for running ProfOcto
│   ├── 01_QUICK_START.md
│   ├── 02_SETUP.md
│   └── 03_PHASE7_USER_GUIDE.md
├── features/              # Feature documentation
│   ├── DEBATE_SYSTEM.md
│   ├── ACADEMIC_RIGOR.md
│   ├── RESEARCH_MODE.md
│   ├── PHASE5_ICLR_PIPELINE.md
│   └── PHASE7_COMPLETION_REPORT.md
├── development/           # Development & configuration
│   ├── CONFIG_REFERENCE.md
│   ├── DEBUGGING.md
│   ├── TESTING.md
│   └── ARCHITECTURE.md
└── archive/               # Legacy documentation (earlier phases)
    ├── ACADEMIC_RIGOR_SYSTEM.md
    ├── DEBUGGING.md
    ├── ENHANCED_RIGOR_SUMMARY.md
    ├── LOGGING_GUIDE.md
    ├── PROMPTS_STRUCTURE.md
    ├── RESEARCH_MODE_GUIDE.md
    └── START_HERE_TESTING.md
```

---

## 📊 Feature Overview

| Phase | Feature          | Status    | Docs                                         |
| ----- | ---------------- | --------- | -------------------------------------------- |
| 1-4   | Debate Engine    | ✅ Active | [Debate System](features/DEBATE_SYSTEM.md)   |
| 1-4   | Research Kit     | ✅ Active | [Research Mode](features/RESEARCH_MODE.md)   |
| 1-4   | Rigor Scoring    | ✅ Active | [Academic Rigor](features/ACADEMIC_RIGOR.md) |
| 5     | ICLR Readiness   | ✅ Active | [Phase 5](features/PHASE5_ICLR_PIPELINE.md)  |
| 6     | Caching & Export | ✅ Active | Config Flags                                 |
| 7     | PhD UX           | ✅ Active | [Phase 7](guides/03_PHASE7_USER_GUIDE.md)    |

---

## 🤖 AI Models

ProfOcto supports all free Gemini models:

- **`Gemma-3-1B`** (Default) — Fastest, best for rapid debates

Change in [config.py](config.py): `MODEL = "gemma-3-1b-it"`

---

## 🔧 Configuration Highlights

Key settings to know:

```python
# Startup behavior
QUICK_START_MODE = True          # Ask only for topic
INTERACTIVE_SETUP = True         # Allow settings refinement

# Show what you want
SHOW_TOP_GAP_DASHBOARD = True    # Prominent #1 gap
ESTIMATE_API_COST = True         # Show cost before running

# Enable features
ENABLE_BOOKMARKING = True        # Save favorite gaps
ENABLE_RUN_HISTORY = True        # Track all debates
ENABLE_PDF_EXPORT = True         # Export for advisor
ENABLE_BATCH_MODE = True         # Run multiple topics

# Full reference: see development/CONFIG_REFERENCE.md
```

---

## 🚀 Quick Commands

```bash
# Run a single debate with Phase 5 analysis
python main.py

# Run test suite
python test_phase7.py

# Custom topic from CLI
python main.py "Your research question here" "Research field"
```

---

## 💡 Key Concepts

**Research Gap** — A problem not yet solved in academic literature, suitable for PhD research

**ICLR Readiness Score** — 0-100 score indicating if a gap is ready for top-tier publication

**Novelty Score** — How novel the gap is vs. state-of-the-art

**Feasibility Score** — How realistic the gap is to solve in 6-18 months

**Elevator Pitch** — Quick 30-second verbal summary for presentations/discussions

---

## 📞 Support

- Check [Debugging Guide](development/DEBUGGING.md) for common issues
- Review configuration flags in [CONFIG_REFERENCE.md](development/CONFIG_REFERENCE.md)
- See test results in [TESTING.md](development/TESTING.md)

---

**Last Updated:** March 17, 2026  
**Phase:** 7 (PhD UX Improvements)  
**Version:** 1.0
