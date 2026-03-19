# Setup & Installation

Detailed instructions for setting up ProfOcto on your machine.

---

## Prerequisites

- **Python 3.10+** — [python.org/downloads](https://www.python.org/downloads/)
- **Gemini API Key** — free from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Node.js 18+** (only required for the Web UI) — [nodejs.org](https://nodejs.org)

---

## Step 1: Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

The free tier provides:

- 15 requests per minute
- 1,000,000 tokens per minute

---

## Step 2: Clone & Install

```bash
# Clone the repository
git clone https://github.com/HZhalex/ProfOcto.git
cd ProfOcto

# Create a virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS / Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies installed** (4 packages):

| Package        | Purpose                                      |
| -------------- | -------------------------------------------- |
| `google-genai` | Gemini API client                            |
| `rich`         | Terminal formatting (panels, tables, colors) |
| `fastapi`      | Web API framework                            |
| `uvicorn`      | ASGI server for FastAPI                      |

---

## Step 3: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` and paste your Gemini API key:

```
GEMINI_API_KEY=AIzaSyD...your-key-here
```

---

## Step 4: Run

### Terminal UI

```bash
python main.py
```

Enter your research topic when prompted. ProfOcto handles everything else with default settings.

You can also pass the topic directly:

```bash
python main.py "MoE vs Dense Models" "Distributed Training"
```

### Web UI (Optional)

You need two terminals running simultaneously:

**Terminal 1 — FastAPI backend:**

```bash
# Make sure the virtual environment is activated
uvicorn web.server:app --reload --port 8000
```

**Terminal 2 — React dev server:**

```bash
cd web
npm install    # first time only
npm run dev
```

Open http://localhost:5173 in your browser.

For production deployment, build the frontend:

```bash
cd web
npm run build
```

After building, FastAPI serves the React frontend automatically from `web/dist/`.

---

## Configuration (Optional)

Edit `config.py` to customize behavior. Key settings:

```python
# AI model (free tier)
MODEL = "gemma-3-1b-it"

# Debate structure
NUM_PROFESSORS = 2              # Panel size (2–5)
MAX_ROUNDS = 1                  # Debate rounds
MAX_TOKENS_PER_TURN = 700       # Response length

# Features
QUICK_START_MODE = True         # Minimal prompts
ESTIMATE_API_COST = True        # Show cost before running
SHOW_TOP_GAP_DASHBOARD = True   # Highlight top gap
ENABLE_BOOKMARKING = True       # Save favorite gaps
ENABLE_PDF_EXPORT = True        # Export for advisor
ENABLE_ELEVATOR_PITCH = True    # Generate verbal summaries

# Caching (~60% cost savings)
USE_RETRY_CACHE = True
CACHE_PHASE5_RESULTS = True
```

See [Configuration Reference](../development/CONFIG_REFERENCE.md) for all 100+ flags.

---

## Directory Structure

After setup and first run, your project will look like:

```
ProfOcto/
├── main.py                 # Entry point
├── config.py               # Configuration (all flags)
├── orchestrator.py         # Professor generation & debate setup
├── .env                    # Your API key (not committed)
├── requirements.txt        # Python dependencies
│
├── agents/                 # 13 AI analysis agents
├── debate/                 # Session state & turn management
├── output/                 # Export & display modules
├── prompts/                # System prompts for AI agents
├── utils/                  # Logging, caching, bookmarking
├── web/                    # Web UI (React + FastAPI)
├── docs/                   # Documentation
│
├── transcripts/            # Saved debate transcripts
├── research_kits/          # Generated research kits
├── logs/                   # Session & debug logs
└── phd_analysis/           # PhD analysis output
    ├── bookmarks.json      #   Bookmarked gaps
    ├── run_history.json    #   Session history
    ├── advisor_reports/    #   Exported reports
    ├── batch_results/      #   Batch processing output
    └── .cache/             #   API result cache
```

---

## Troubleshooting

### API Key Error

- Verify `.env` file exists in the project root (not in a subfolder)
- Ensure the key is correct — copy it again from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Check there are no extra spaces or quotes around the key

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

Make sure you're using the virtual environment (`.venv`) and not the system Python.

### Permission Errors (Windows)

Run your terminal as Administrator, or use:

```bash
pip install --user -r requirements.txt
```

### Rate Limiting (429 errors)

The free tier allows 15 requests per minute. If you hit rate limits:

- Wait 60 seconds and try again
- Reduce `NUM_PROFESSORS` to 2 in `config.py`
- Reduce `MAX_ROUNDS` to 1

---

## Next Steps

1. **Run your first analysis**: `python main.py`
2. **Explore features**: [Feature Guide](03_PHASE7_USER_GUIDE.md)
3. **Customize settings**: [Configuration Reference](../development/CONFIG_REFERENCE.md)
4. **Try the Web UI**: [Web UI Guide](../../web/README_WEB.md)
