# Academic Rigor System for Research AI Assistant

## Overview

This system transforms your debate arena into a **rigorous research AI assistant** that enforces mathematical backing for ALL claims. It's designed specifically for PhD-level research in mathematical domains like Implicit Neural Representations.

## Problem Solved

**Before:** Debates were conceptual but vague. Claims lacked mathematical grounding.

- Professor A: "Fourier features are better"
- Professor B: "No, learnable activations are better"
- Missing: Which theorems support each position? What are the bounds? What are the assumptions?

**After:** Debates are mathematically rigorous. Every claim must cite papers and theorems.

- Professor A: "Fourier Feature Networks (Tancik et al., 2020) achieve O(L) feature dimension where L is the number of frequency levels. This provides better spectral coverage compared to ReLU networks which have spectral bias (Rahaman et al., 2019)"
- Professor B: "However, Barron space complexity (Barron, 1993) shows sample complexity grows as O(d·1/ε²). Natural images aren't in Barron space, so while sinc basis helps frequencies, we still need learnable activations like in SIREN (Sitzmann et al., 2020) to achieve polynomial convergence rates"

## System Architecture

### Layer 1: Professor Rigor Enforcement

**File:** `prompts/system/professor_rigor.txt`

When `ACADEMIC_RIGOR_MODE = True`, professors load this system prompt which requires:

1. **Explicit Paper Citations** with year (Author, Year) format
2. **Mathematical Statements** - the actual theorem, bound, or formula
3. **Assumptions & Boundary Conditions** - when does this theorem break down?
4. **Complexity/Convergence Bounds** - what are the quantitative properties?

**Config Flag:**

```python
# config.py
ACADEMIC_RIGOR_MODE = True  # Enforce mathematical backing in debates
```

### Layer 2: Foundational Paper Extraction

**Function:** `academic_validator.extract_foundational_papers()`
**Output:** `[topic]_foundational_papers.json`

Extracts:

- **Field title and research directions** - what are the main areas of INR research?
- **Foundational papers** (8-10 key papers) with:
  - Title, authors, year
  - Core contribution
  - Theorems/frameworks introduced
  - Why it's foundational
  - Relevance to current topic
- **Core theorems** - which mathematical results are central?

Example for Implicit Neural Representations:

```json
{
  "field_title": "Implicit Neural Representations (INRs)",
  "research_directions": [
    "Function approximation in high dimensions",
    "Coordinate-based neural networks",
    "Spectral properties of neural networks"
  ],
  "foundational_papers": [
    {
      "title": "Implicit Neural Representations with Levels-of-Experts",
      "authors": "Sitzmann et al.",
      "year": 2020,
      "contribution": "SIREN architecture with learnable sine activations for better frequency coverage",
      "theorem_or_framework": "Spectral bias mitigation through learnable frequency initialization",
      "significance": "Shows that sinc basis alone isn't sufficient; learnable activations needed",
      "relevance_to_topic": "Central to understanding limitations of fixed-basis INRs"
    }
  ],
  "core_theorems": [
    {
      "name": "Spectral Bias Theorem",
      "paper": "Rahaman et al., 2019",
      "statement": "Neural networks with ReLU activations preferentially learn low frequencies first",
      "implications": "Fixed-basis INRs struggle with high-frequency details; learnable activations help"
    }
  ]
}
```

### Layer 3: Mathematical Claim Verification

**Function:** `academic_validator.verify_mathematical_claims()`
**Output:** `[topic]_verified_claims.json`

Takes key findings from the debate and verifies:

1. Does it have mathematical backing? (theorem, proof, bound, formula)
2. Which paper supports it?
3. What assumptions does it rely on?
4. Are there boundary conditions?

Categorizes claims as:

- **MATHEMATICALLY_BACKED** - Has clear theorem/proof/bounds support
- **NEEDS_PROOF** - Sensible but missing mathematical foundation
- **UNSUPPORTED** - No clear mathematical basis
- **CONTRADICTS** - Conflicts with established theorem

Result example:

```json
{
  "valid_claims": [
    {
      "claim": "Positional encoding improves INR approximation of high frequencies",
      "backing": "Spectral Bias Theorem + Tancik et al. empirical validation",
      "paper": "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains",
      "mathematical_statement": "Fourier positional encoding maps input x to (sin(2^0 πx), cos(2^0 πx), ..., sin(2^L πx), cos(2^L πx)) creating O(L) features spanning frequency range [2^0, 2^L]",
      "assumptions": [
        "Target function is band-limited or approximable by Fourier series",
        "Frequency coverage [2^0, 2^L] contains signal content"
      ]
    }
  ],
  "unverified_claims": [
    {
      "claim": "Learnable activations always outperform fixed basis",
      "why_unverified": "No formal theorem comparing all activation types under controlled settings",
      "suggested_backing": "Need complexity analysis or convergence rate bounds for comparison"
    }
  ]
}
```

### Layer 4: Citation Tracking

**Function:** `academic_validator.track_citations()`
**Output:** `[topic]_citation_analysis.json`

Builds citation network:

1. **Which papers each professor cites** (explicit or conceptual)
2. **Which theorems are actively used in arguments**
3. **How arguments build on each other**
4. **Gaps where claims lack citation**

Example:

```json
{
  "citation_map": {
    "Dr. Chen": [
      {
        "paper": "Fourier Features Let Networks Learn..., 2020",
        "mentions": 3,
        "usage": "Using Fourier basis dimension to argue frequency coverage"
      },
      {
        "paper": "Spectral Bias and Kernel Ridge Regression, 2019",
        "mentions": 2,
        "usage": "Explaining why sinc basis needs augmentation"
      }
    ]
  },
  "argument_chains": [
    {
      "thesis": "SIREN outperforms fixed-basis INRs",
      "supporting_claims": [
        {
          "claim": "ReLU networks have spectral bias",
          "paper_backing": "Rahaman et al., 2019",
          "theorem_used": "Spectral Bias Theorem"
        },
        {
          "claim": "Sine activations learn higher frequencies faster",
          "paper_backing": "Sitzmann et al., 2020",
          "theorem_used": "SIREN activation analysis"
        }
      ]
    }
  ]
}
```

### Layer 5: Debate Rigor Assessment

**Function:** `academic_validator.validate_debate_rigor()`
**Output:** `[topic]_debate_rigor.json`

Evaluates:

- **Rigor score** (1-10)
- **Strengths** - what was well-grounded?
- **Weaknesses** - what was vague?
- **Missing elements** - what theorems should have been discussed?
- **PhD-level assessment** - is this suitable for dissertation?
- **Next steps** - how to deepen for dissertation

Result:

```json
{
  "rigor_score": 8,
  "strengths": [
    "Clear citation of Tancik et al. frequency analysis",
    "Discussion of spectral bias with reference to Rahaman et al.",
    "Concrete complexity O(L) for Fourier features"
  ],
  "weaknesses": [
    "Missing complexity analysis of learnable activation training",
    "Vague statements about 'fitting details' without bounds",
    "No discussion of approximation error rates"
  ],
  "missing_elements": [
    "Barron space complexity bounds",
    "Convergence rate proofs for SIREN",
    "Sample complexity comparisons"
  ],
  "recommendation": "Add theoretical bounds comparing ReLU vs sine activations. Cite convergence rate results.",
  "is_phd_level": true,
  "next_steps_for_dissertation": "Use this debate to identify gaps in INR theory. Focus on formalizing claims about frequency representation."
}
```

## Usage

### Running with Academic Rigor

```python
# In config.py - already enabled by default
ACADEMIC_RIGOR_MODE = True
RESEARCH_MODE = True

# Run debate
python main.py
# Topic: "Implicit Neural Representations: Fourier basis vs learnable activations"
# Field: "Neural Network Theory & Coordinate-Based Representations"
```

### Generated Files

After debate, you'll get:

1. **Debate transcript** - `transcripts/debate_*.md`
2. **Research kit** (14 comprehensive analyses):
   - `_outline.md` - paper structure
   - `_foundational_papers.json` - key papers for field
   - `_verified_claims.json` - which claims have backing
   - `_citation_analysis.json` - citation network
   - `_debate_rigor.json` - rigor assessment
   - ... (plus 9 other mathematical & academic analyses)

### Accessing Results Programmatically

```python
from agents.research_synthesizer import generate_research_kit, save_research_kit

# After debate session
kit = generate_research_kit(session, topic, field)

# Save all 19 output files
kit_file = save_research_kit(kit, "research_kits")

# Access specific analyses
foundational_papers = kit["foundational_papers"]
verified_claims = kit["verified_claims"]
citation_analysis = kit["citation_analysis"]
debate_rigor = kit["debate_rigor"]

# Use for dissertation
for paper in foundational_papers["foundational_papers"]:
    print(f"Must cite: {paper['title']} ({paper['year']})")

# Identify what needs proving
for claim in verified_claims["unverified_claims"]:
    print(f"Need to prove: {claim['claim']}")
```

## Comparison: Rigor vs Non-Rigor

### Non-Rigorous Statement

> "Fourier features are better because they help with high-frequency details. Several papers have shown this."

**Problem:**

- No specific paper cited
- "High-frequency details" is vague
- No bounds or complexity
- No assumptions stated

### Rigorous Statement

> "In Fourier Feature Networks (Tancik et al., 2020), positional encoding maps x ∈ R^d to (sin(2^0 πx), cos(2^0 πx), ..., sin(2^L πx), cos(2^L πx)) ∈ R^{2Ld}.
> This achieves O(L) feature dimension spanning frequencies [2^0, 2^L].
> The key theorem is the Spectral Bias result (Rahaman et al., 2019): standard ReLU networks preferentially learn low frequencies first, requiring O(ω²/ε) samples for frequency ω.
> By explicitly including high frequencies, Fourier positional encoding achieves polynomial rather than exponential sample complexity.
> However, this ONLY works for band-limited or bandpass-approximable functions - natural images aren't band-limited (non-zero frequency content everywhere), which is why Tancik et al.'s empirical results show Fourier features still struggle with sharp edges unless combined with learnable activations as in SIREN (Sitzmann et al., 2020)."

**Strengths:**

- Specific papers with years
- Mathematical statement (mapping + complexity)
- Cites relevant theorems
- States assumptions (band-limited functions)
- Acknowledges limitations
- Connects to follow-up work (SIREN)
- Could be directly cited in dissertation

## Configuration

```python
# config.py
ACADEMIC_RIGOR_MODE = True        # Enforce mathematical backing
RESEARCH_MODE = True              # Generate research kit
MAX_ROUNDS = 2                    # Debate length
NUM_PROFESSORS = 3                # Panel size
GEMINI_API_KEY = "..."           # API key
```

## For Your Dissertation on INRs

This system helps by:

1. **Extracting foundational papers** you must cite
2. **Verifying claims** have mathematical backing
3. **Building citation network** showing how papers relate
4. **Assessing rigor** of arguments
5. **Identifying gaps** that need theorems/proofs
6. **Generating rigorous debate** vs vague speculation

Use the debate to:

- Identify unexplored areas (research gaps)
- Understand how papers connect
- Find open problems that are mathematically well-defined
- Strengthen arguments for your dissertation

## Future Enhancements

1. **Proof sketches** - Generate formal proof outlines
2. **Complexity certificates** - Automatically verify Big-O claims
3. **Paper similarity** - Find related work in citation network
4. **Open problem mining** - Extract unsolved problems from debates
5. **LaTeX theorem generation** - Auto-format theorems for dissertation
