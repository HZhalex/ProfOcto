# Installation & Setup

Get ProfOcto running in 5 minutes.

## Prerequisites

- **Python 3.8+**
- **Gemini API Key** (free from [Google AI Studio](https://aistudio.google.com/app/apikey))
  - **Free Tier Models Available:**
  - **Rate Limits:** 15 requests/min, 1M tokens/minute on free tier

---

## Step 1: Get API Key (1 minute)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

---

## Step 2: Clone & Setup (2 minutes)

```bash
# Clone repository
git clone https://github.com/HZhalex/ProfOcto.git
cd ProfOcto

# Create .env file with your API key
echo "GEMINI_API_KEY=your-key-here" > .env

# Install dependencies
pip install -r requirements.txt
```

---

## Step 3: Verify Setup (1 minute)

```bash
# Run test suite to verify everything works
python test_phase7.py
```

You should see:

```
==============================
✓ PASS: Module Imports
✓ PASS: Config Flags
✓ PASS: Cost Estimator
✓ PASS: Bookmark System
✓ PASS: Elevator Pitch
✓ PASS: Dashboard
✓ PASS: PDF Exporter

Total: 7/7 tests passed
==============================
```

---

## Switching Models

Edit [config.py](../../config.py) to change the default model:

```python
MODEL = "gemma-3-1b-it"
```


## Step 4: Run First Analysis (3 minutes)

```bash
python main.py
```

Enter your research topic and let ProfOcto analyze it!

---

## Configuration (Optional)

Edit `config.py` to customize behavior:

```python
# Startup
QUICK_START_MODE = True          # Ask topic only
INTERACTIVE_SETUP = True         # Allow inline refinement

# Features
ESTIMATE_API_COST = True         # Show cost before running
SHOW_TOP_GAP_DASHBOARD = True   # Highlight #1 gap
ENABLE_BOOKMARKING = True        # Save favorite gaps
ENABLE_PDF_EXPORT = True         # Export for advisor
ENABLE_ELEVATOR_PITCH = True     # Generate pitches

# Performance
USE_RETRY_CACHE = True           # 60% API cost savings
FAST_MODE = False                # Skip optional features
```

[→ Full config reference](../development/CONFIG_REFERENCE.md)

---

## Troubleshooting

### API Key Error

- Verify `.env` file exists and is in root directory
- Check key is correct (copy from [Google AI Studio](https://aistudio.google.com/app/apikey))
- Regenerate key if needed

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Permission Errors

```bash
# On Windows, run as administrator:
pip install -r requirements.txt

# On Mac/Linux:
sudo pip install -r requirements.txt
```

---

## Directory Structure

After setup, you'll have:

```
ProfOcto/
├── main.py                 # Main entry point
├── config.py              # Configuration
├── orchestrator.py        # Debate engine
├── agents/                # AI agent modules
├── output/                # Output generation
├── docs/                  # User documentation
├── phd_analysis/          # Results & cache
│   ├── logs/
│   ├── bookmarks.json
│   ├── run_history.json
│   ├── advisor_reports/
│   └── .cache/
└── requirements.txt       # Dependencies
```

---

## Next Steps

1. **Run first analysis:** `python main.py`
2. **Read user guide:** [Phase 7 Features](03_PHASE7_USER_GUIDE.md)
3. **Bookmark gaps:** Tag your favorites for later
4. **Export to advisor:** Share analysis as PDF
5. **Generate pitch:** Create 30-sec explanation

---

**Help:** Check [Debugging Guide](../development/DEBUGGING.md) or [Docs Index](../README.md)
