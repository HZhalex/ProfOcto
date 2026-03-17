# Academic Debate Arena - Testing Guide

## ✅ System Status: READY FOR TESTING

All enhanced components are operational:

- ✅ Gap-Foundation-Solution framework
- ✅ Evidence strength validation (3-5+ papers required)
- ✅ Research topic library (6 topics, 3 INR-specific)
- ✅ 23 output analysis files per debate

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Select a Research Topic

```bash
python select_topic.py
```

Choose one of the 6 topics:

- **[1-3]** INR-specific topics (your domain)
- **[4-6]** General neural network topics

Upon selection, the system will display:

- Research gaps for that topic
- Foundational papers you should know
- Key concepts to debate

### Step 2: Run the Academic Debate

```bash
python main.py
```

The system will:

1. Load your selected topic configuration
2. Initialize 2 professor agents (with ACADEMIC_RIGOR enforced)
3. Generate real-time debate with Gap-Foundation-Solution structure
4. Stream output to console
5. Generate 23 analysis files in `research_kits/[topic]/`

Expected runtime: **10-30 minutes** (depends on API response times)

### Step 3: Examine Generated Analysis Files

Key new files showing enhanced rigor:

**Evidence Strength Validation:**

```bash
cat research_kits/research_kit_[topic_name]/_evidence_strength.json
```

Shows:

- Which claims are "strong" (4-5+ papers backing)
- Which claims are "weak" (1-2 papers or theoretical only)
- Evidence gaps where more papers are needed
- Overall score: 0-10

**Gap-Foundation-Solution Analysis:**

```bash
cat research_kits/research_kit_[topic_name]/_gap_foundation_solution.json
```

Shows:

- Did each professor identify research gaps?
- Did they support gaps with mathematical foundation?
- Did they propose concrete solutions?
- Did they acknowledge remaining unsolved gaps?
- Completeness scores for each argument

---

## 📊 What You'll See

### In Console (Real-time):

```
[PROFESSOR A] identifies gap: "Current INRs struggle with..."
[PROFESSOR A] provides math foundation: "Based on Fourier analysis..."
[PROFESSOR A] proposes solution: "We can apply theorem X to..."

[PROFESSOR B] counters with gap: "But your solution has..."
[PROFESSOR B] with foundation: "As proven in [4-5 papers]..."
```

### In Generated JSON:

```json
{
  "strong_claims": [
    { "claim": "SIREN outperforms Fourier features", "papers": 5, "authors": 3 }
  ],
  "weak_claims": [{ "claim": "INRs will replace rasters", "papers": 0 }],
  "evidence_scores": [{ "claim": "...", "score": 8.5 }]
}
```

---

## 🎯 Testing Checklist

After running a debate, verify:

- [ ] Debate completes without errors
- [ ] Console shows Gap-Foundation-Solution structure in arguments
- [ ] 23 output files generated in `research_kits/[topic]/`
- [ ] `_evidence_strength.json` exists and contains scores
- [ ] `_gap_foundation_solution.json` exists and contains analysis
- [ ] Strong claims have 3-5+ papers backing
- [ ] Weak claims are properly identified and scored low
- [ ] Both professors stay on topic
- [ ] Mathematical foundations are discussed

---

## 📁 Output Files Structure

Per debate, you get:

**Debate Transcript:**

- `debate_[topic]_[timestamp].md` - Full conversation

**Academic Analysis (23 files):**

1. `_evidence_strength.json` ← **NEW** - Evidence validation
2. `_gap_foundation_solution.json` ← **NEW** - Structure validation
   3-23. Other research syntheses (research gaps, mathematical frameworks, etc.)

---

## ⚙️ Configuration

Default settings in `config.py`:

```python
ACADEMIC_RIGOR_MODE = True          # Enforces Gap-Foundation-Solution
RESEARCH_MODE = True                 # Generates analysis kit
NUM_PROFESSORS = 2                   # Number of debaters
MAX_ROUNDS = 3                       # Debate turns per professor
```

To modify debate parameters:

```bash
# Edit config.py and change values, then re-run main.py
nano config.py  # or use your editor
python main.py
```

---

## 🔬 Example Test Scenario

**Best Topic for First Test:** `[1] INR: Fixed Encoding vs Learnable Activations`

Why?

- Most relevant to your research domain
- Rich literature (SIREN, NeRF, Fourier Features)
- Clear research gaps (spectral bias, frequency coverage)
- Multiple competing approaches to debate

**Expected Output:**

- 30-40 min debate runtime
- 200+ claims in transcript
- 4-5+ papers cited per strong claim
- Clear Gap-Foundation-Solution structure in arguments

---

## 🐛 Troubleshooting

| Issue                            | Solution                                               |
| -------------------------------- | ------------------------------------------------------ |
| `ModuleNotFoundError: genai`     | Run: `pip install google-generativeai`                 |
| Debate takes >30 min             | Normal - API responses can be slow                     |
| No output files generated        | Check `research_kits/` folder exists                   |
| Evidence strength shows 0 papers | Claims may be theoretical - check JSON for explanation |
| `professor_rigor.txt` not found  | Ensure `prompts/system/` folder exists                 |

---

## 📚 Understanding the Output

### Evidence Strength Score (0-10)

- **9-10**: Excellent (4-5+ papers, diverse authors, recent + foundational)
- **7-8**: Good (3-4 papers, 2-3 authors, temporal diversity)
- **5-6**: Adequate (2-3 papers, some diversity)
- **3-4**: Weak (1-2 papers, limited diversity)
- **0-2**: Unsupported (0 papers, pure speculation)

### Gap-Foundation-Solution Completeness

- **Strong (0.9-1.0)**: Gap identified → Math foundation → Solution → Remaining gaps
- **Partial (0.5-0.8)**: Missing one or two components
- **Weak (0.0-0.4)**: Mostly vague assertions

---

## 🎓 Using Results for Your Dissertation

Export the best debates:

```bash
# Find strongest arguments
grep -A 5 "evidence_scores" research_kits/*/
_evidence_strength.json

# Identify research gaps
grep "research_gaps" research_kits/*/_gap_foundation_solution.json

# Generate citation list
python -c "
import json
topics = json.load(open('research_topics.json'))
for topic in topics:
    print(f\"\\n{topic['title']}:\")
    for paper in topic['foundational_papers'][:3]:
        print(f\"  - {paper}\")
"
```

---

## ✨ Next Steps After First Test

1. **If satisfied with rigor:** Use debates for dissertation background
2. **If want more rounds:** Increase `MAX_ROUNDS` in config.py
3. **If want more professors:** Increase `NUM_PROFESSORS` in config.py
4. **If want different topic:** Run `select_topic.py` again
5. **If want to fine-tune:** Edit `prompts/system/professor_rigor.txt`

---

**Ready to test?**

Start with:

```bash
python select_topic.py
```

Then:

```bash
python main.py
```

Good luck! 🚀
