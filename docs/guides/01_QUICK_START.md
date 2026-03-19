# 🚀 Quick Start Guide (5 Minutes)

Get ProfOcto running and analyze your first research gap in 5 minutes.

## Prerequisites

- Python 3.8+
- Gemini API key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))
  - Free tier: `gemini-2.0-flash` or `gemini-1.5-flash` recommended
  - Rate limit: 15 requests/min, 1M tokens/min

## 1. Setup (2 minutes)

```bash
# Clone or download ProfOcto
cd ProfOcto

# Create .env file with your API key
echo "GEMINI_API_KEY=your-key-here" > .env

# Install dependencies
pip install -r requirements.txt
```

## 2. Run Your First Analysis (3 minutes)

```bash
python main.py
```

You'll be asked just **one question**:

```
🎯 Research Gap Analysis
What research topic or problem would you like to explore?
> [Your research question here]
```

Then ProfOcto will:

1. ✅ Create multi-professor debate on your topic (~2-3 min)
2. ✅ Identify research gaps
3. ✅ Run Phase 5 ICLR readiness pipeline (~2-3 min)
4. ✅ Show top gap on dashboard
5. 📊 Display cost estimate

## 3. What You'll See

### Cost Estimate (before running)

```
📊 Estimated Cost & Timeline:
  • API Cost: $0.87
  • Runtime: 2.7 minutes
```

### Top Gap Dashboard (after finishing)

```
╔════════════════════════════════════════════════════════════════╗
║ TOP GAP #1 (RECOMMENDED FOR PURSUIT)                          ║
║ Your top research opportunity...                              ║
║ ✅ Readiness: 85/100                                         ║
║ 📊 Novelty: 80/100 | Feasibility: 85/100                    ║
║ ⏱️  Timeline: ~6 months                                       ║
╚════════════════════════════════════════════════════════════════╝
```

### Interactive Menu

```
🔍 Explore gaps interactively?
[2] 📌 Bookmark your favorite gap
[3] 🚀 Export gap analysis for advisor
[4] 💬 Generate elevator pitch
[5] 📋 Compare with previous runs
```

## 4. What to Do Next

**Option A: Share with Advisor**

```
[3] 🚀 Export gap analysis for advisor
# Creates PDF/TXT file with full analysis
```

**Option B: Get Elevator Pitch**

```
[4] 💬 Generate elevator pitch
# 30-second summary for presentations
```

**Option C: Save for Later**

```
[2] 📌 Bookmark your favorite gap
# Saved in phd_analysis/bookmarks.json
```

## 5. Customization (Optional)

Want to adjust settings before running?

```
⚙️  Customize settings before running? [y/N]: y

Options:
  [1] Change topic
  [2] Change field
  [3] Toggle Phase 5 analysis
  [5] Skip optional features (fast mode)
```

---

## 📁 Files & Output

After running, you'll find:

```
phd_analysis/
├── logs/                    # Debate logs
├── bookmarks.json          # Your saved gaps
├── run_history.json        # All past debates
├── advisor_reports/        # PDF exports
├── batch_results/          # Batch processing results
└── .cache/                 # API result cache (60% cost savings!)
```

---

## ⚡ Speed Tips

**Too slow?** Enable fast mode:

```
[5] Skip optional features (fast mode)
# Cuts runtime by 30-40%
```

**Too expensive?** Set budget:

```python
# In config.py:
COST_CONFIRMATION_THRESHOLD = 0.25  # Ask before $0.25+
```

---

## 🐛 Troubleshooting

### "API key error"

- Check `.env` file has correct key
- Regenerate key at [Google AI Studio](https://aistudio.google.com/app/apikey)

### "Cost too high"

- Caching is ON by default (60% savings)
- Use FAST_MODE for optional features skip
- Reduce `NUM_PROFESSORS` in config.py

### "Dashboard not showing"

- Check Phase 5 completed (see logs)
- Verify `SHOW_TOP_GAP_DASHBOARD = True` in config

---

## 📖 Next Steps

- **Learn all features:** See [Phase 7 User Guide](03_PHASE7_USER_GUIDE.md)
- **Configure everything:** See [Config Reference](../development/CONFIG_REFERENCE.md)
- **Run multiple debates:** Use batch mode (ENABLE_BATCH_MODE = True)
- **Understand the code:** See [Architecture](../development/ARCHITECTURE.md)

---

**Stuck?** Check [Debugging Guide](../development/DEBUGGING.md)
