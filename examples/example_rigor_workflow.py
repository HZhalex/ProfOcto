"""
Example: Using Academic Rigor System for INR Research
Shows how to run debates with mathematical backing enforcement
"""

import json
from debate.session import DebateSession, ProfessorProfile, Turn
from agents.research_synthesizer import generate_research_kit, save_research_kit
from agents import academic_validator
import config

# ============================================================================
# STEP 1: Setup Configuration with Academic Rigor
# ============================================================================

print("=" * 70)
print("STEP 1: Configuration")
print("=" * 70)

config.ACADEMIC_RIGOR_MODE = True  # Enforce theorem-backed arguments
config.RESEARCH_MODE = True        # Generate comprehensive research kit
config.MAX_ROUNDS = 2
config.NUM_PROFESSORS = 2

print(f"Academic Rigor Mode: {config.ACADEMIC_RIGOR_MODE}")
print(f"Research Mode: {config.RESEARCH_MODE}")
print("Professors will be required to cite papers and theorems")
print()

# ============================================================================
# STEP 2: Create Debate Session with Expert Professors
# ============================================================================

print("=" * 70)
print("STEP 2: Create Expert Professors")
print("=" * 70)

# Professor 1: Fixed-basis proponent
prof_fixed = ProfessorProfile(
    key="prof_tancik",
    name="Dr. Tancik",
    university="UC Berkeley",
    role="Theorist",
    expertise="Neural Radiance Fields, Positional Encoding",
    personality="methodical, mathematical",
    stance="Fixed positional encoding (Fourier features) provides theoretical guarantees",
)

# Professor 2: Learnable activation proponent
prof_learnable = ProfessorProfile(
    key="prof_sitzmann",
    name="Dr. Sitzmann",
    university="MIT",
    role="Pragmatist",
    expertise="Implicit Representations, Activation Functions",
    personality="rigorous, empirical",
    stance="Learnable activations (SIREN) needed for practical performance",
)

print(f"✓ {prof_fixed.name} ({prof_fixed.university})")
print(f"  Expertise: {prof_fixed.expertise}")
print()
print(f"✓ {prof_learnable.name} ({prof_learnable.university})")
print(f"  Expertise: {prof_learnable.expertise}")
print()

# ============================================================================
# STEP 3: Define Research Topic (Implicit Neural Representations)
# ============================================================================

print("=" * 70)
print("STEP 3: Define Research Topic")
print("=" * 70)

topic = "Implicit Neural Representations: Fixed Positional Encoding vs Learnable Activations"
field = "Neural Network Theory & Coordinate-Based Representations"

print(f"Topic: {topic}")
print(f"Field: {field}")
print()
print("Key research questions:")
print("1. Should INRs use fixed Fourier bases or learnable activations?")
print("2. What are the theoretical guarantees for each approach?")
print("3. What are the approximation error bounds?")
print("4. What foundational papers establish the framework?")
print()

# ============================================================================
# STEP 4: Create Session and Add Mock Turns
# ============================================================================

print("=" * 70)
print("STEP 4: Simulate Debate with Mathematical Arguments")
print("=" * 70)

session = DebateSession(topic=topic, field=field)
session.add_professor(prof_fixed)
session.add_professor(prof_learnable)

# Simulate opening turns with mathematical backing
turn1 = Turn(
    turn_number=1,
    speaker_key="prof_tancik",
    speaker_name="Dr. Tancik",
    role="Theorist",
    content="""Fourier Feature Networks (Tancik et al., 2020) use positional encoding 
    that maps x to [sin(2⁰πx), cos(2⁰πx), ..., sin(2ᴸπx), cos(2ᴸπx)]. 
    This creates O(L) features spanning frequencies [2⁰, 2ᴸ]. 
    The key theorem is the Spectral Bias result (Rahaman et al., 2019): 
    standard networks learn low frequencies exponentially faster, requiring O(ω²/ε) samples. 
    Fourier positional encoding achieves polynomial rather than exponential sample complexity 
    for band-limited functions.""",
)

turn2 = Turn(
    turn_number=2,
    speaker_key="prof_sitzmann",
    speaker_name="Dr. Sitzmann",
    role="Pragmatist",
    content="""I agree Fourier features help, but they have limitations. 
    Natural images are NOT band-limited (non-zero frequency everywhere). 
    SIREN (Sitzmann et al., 2020) uses learnable sine activations and achieves 
    better practical results. The convergence proof in our paper shows 
    sin activations converge O(ln(1/ε)) times faster than ReLU. 
    While Tancik's Fourier encoding covers frequency range [2⁰, 2ᴸ], 
    we still need learnable weights on activation frequencies for non-bandlimited signals.""",
)

turn3 = Turn(
    turn_number=3,
    speaker_key="prof_tancik",
    speaker_name="Dr. Tancik",
    role="Theorist",
    content="""SIREN's convergence analysis assumes smooth targets. For images with sharp edges, 
    you need higher frequencies than [2⁰, 2ᴸ] fixed range. But my point: 
    Fourier positional encoding + ANY neural network gives O(κd/ε) sample complexity 
    by Barron space theory (Barron, 1993), while SIREN achieves O(d·poly(log(1/ε))). 
    Both suffer curse of dimensionality in d. The question is: 
    for practical image fitting, which is more sample-efficient when dimension matters?""",
)

session.add_turn(turn1)
session.add_turn(turn2)
session.add_turn(turn3)

print(f"✓ Created session with {len(session.turns)} debate turns")
print(f"✓ Total professors: {len(session.professors)}")
print()

# ============================================================================
# STEP 5: Generate Comprehensive Research Kit
# ============================================================================

print("=" * 70)
print("STEP 5: Generate Research Kit with Academic Rigor")
print("=" * 70)
print("Analyzing debate for:")
print("  - Foundational papers in the field")
print("  - Mathematical claims and backing")
print("  - Citation network")
print("  - Debate rigor assessment")
print("  - [+ 15 other analyses]")
print()

# Note: In production, this would call the actual Gemini API
# For this example, we show the structure
print("Research kit will include:")
print("  1. foundational_papers.json - Key papers for the field")
print("  2. verified_claims.json - Which claims have mathematical backing")
print("  3. citation_analysis.json - Citation network diagram")
print("  4. debate_rigor.json - Rigor assessment (1-10 score)")
print("  5. [+ 15 other mathematical & academic analyses]")
print()

# ============================================================================
# STEP 6: Show What the System Extracts
# ============================================================================

print("=" * 70)
print("STEP 6: Example Research Kit Contents")
print("=" * 70)

example_foundational = {
    "field_title": "Implicit Neural Representations (INRs)",
    "foundational_papers": [
        {
            "title": "Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains",
            "authors": "Tancik et al.",
            "year": 2020,
            "contribution": "Positional encoding with Fourier features for INRs",
            "theorem_or_framework": "Spectral bias + frequency coverage analysis",
        },
        {
            "title": "Implicit Neural Representations with Levels-of-Experts",
            "authors": "Sitzmann et al.",
            "year": 2020,
            "contribution": "Learnable sine activations (SIREN) for better convergence",
            "theorem_or_framework": "Convergence rate O(ln(1/ε)) for smooth targets",
        },
    ]
}

example_verified = {
    "valid_claims": [
        {
            "claim": "Fourier positional encoding achieves O(L) feature dimension",
            "backing": "Tancik et al. mathematical specification",
            "mathematical_statement": "Encoding: (sin(2^0 πx), cos(2^0 πx), ..., sin(2^L πx), cos(2^L πx))",
        },
        {
            "claim": "SIREN converges faster than ReLU + Fourier",
            "backing": "SIREN convergence analysis theorem",
            "mathematical_statement": "Convergence rate: O(ln(1/ε)) vs exponential for standard networks",
        },
    ],
    "unverified_claims": [
        {
            "claim": "SIREN is more sample-efficient for natural images",
            "why_unverified": "No formal sample complexity analysis for non-bandlimited signals",
            "suggested_backing": "Derivation of VC dimension or Rademacher complexity bounds",
        },
    ]
}

example_rigor = {
    "rigor_score": 8,
    "is_phd_level": True,
    "strengths": [
        "Explicit citation of Tancik et al. and Sitzmann et al. with years",
        "Mathematical specifications of Fourier encoding",
        "Discussion of spectral bias with reference to Rahaman et al.",
        "Convergence rate bounds quoted with specific results",
    ],
    "weaknesses": [
        "Missing sample complexity bounds for non-bandlimited regime",
        "Vague claim about 'practical performance' without metrics",
        "Barron space mentioned but not fully explored",
    ],
    "next_steps_for_dissertation": [
        "Derive sample complexity for SIREN on natural image distributions",
        "Formalize 'bandlimited approximation' for practical images",
        "Compare approximation error rates empirically with theory",
    ]
}

print("\nFOUNDATIONAL PAPERS:")
print(json.dumps(example_foundational, indent=2))

print("\nVERIFIED CLAIMS:")
print(json.dumps(example_verified, indent=2))

print("\nRIGOR ASSESSMENT:")
print(json.dumps(example_rigor, indent=2))

print()

# ============================================================================
# STEP 7: How to Use Results for Your Dissertation
# ============================================================================

print("=" * 70)
print("STEP 7: Using Results for PhD Dissertation")
print("=" * 70)

print("""
After running debate with ACADEMIC_RIGOR_MODE = True:

1. FOUNDATIONAL PAPERS
   - Use these to structure your literature review
   - Identify which papers are MUST-CITE for your work
   - Understand research direction evolution

2. VERIFIED CLAIMS
   - Identify which arguments have mathematical backing
   - Find unverified claims that need proofs
   - Use verified claims as citations in your dissertation

3. CITATION ANALYSIS
   - Understand how papers relate to each other
   - Build your citation network visualization
   - Identify missing connections between areas

4. RIGOR ASSESSMENT
   - Know your debate achieved PhD-level rigor
   - Use feedback to strengthen your own arguments
   - Identify missing mathematical elements

5. RESEARCH GAPS
   - Find unexplored theoretical territories
   - Identify open problems that are mathematically well-defined
   - Propose dissertation research directions

CONCRETE EXAMPLE:
- Debate identified: "Sample complexity for SIREN on natural images unknown"
- This becomes a RESEARCH GAP
- You can now propose: "I will derive sample complexity bounds for..."
- This is PhD-level contribution!
""")

print()

# ============================================================================
# STEP 8: Next Steps
# ============================================================================

print("=" * 70)
print("STEP 8: How to Run Your Own Debate")
print("=" * 70)

print("""
1. Run via CLI:
   python main.py
   (Select theme: "Implicit Neural Representations: ...")

2. Run via Web UI:
   # Start server (in separate terminal)
   cd web && python server.py
   # Open http://localhost:8000
   # Click "Start Debate" button

3. Access Results Programmatically:
   python -c "
   from agents.research_synthesizer import generate_research_kit
   # After debate session
   kit = generate_research_kit(session, topic, field)
   
   # Access analyses
   papers = kit['foundational_papers']
   claims = kit['verified_claims']
   citations = kit['citation_analysis']
   rigor = kit['debate_rigor']
   
   # ...use for dissertation
   "

4. Configuration:
   # config.py
   ACADEMIC_RIGOR_MODE = True  # MUST BE TRUE for rigor
   RESEARCH_MODE = True
   NUM_PROFESSORS = 2-5  # Adjust panel size
   MAX_ROUNDS = 2-4      # Adjust debate length
""")

print()

# ============================================================================
# Summary
# ============================================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
✓ Academic Rigor System Implemented
  - Professors enforce theorem-backed arguments
  - Extract foundational papers automatically
  - Verify mathematical claims with backing
  - Track citations and argument chains
  - Assess debate rigor on PhD-level
  - Generate 19 analysis files per debate

✓ System Ready for Implicit Neural Representations
  - Debate on: Fixed basis vs learnable activations
  - Mathematical depth: theorems, bounds, complexity
  - Output: papers, verified claims, citations, rigor score
  - Use for: dissertation planning, literature review, research gaps

✓ Next: Run Debate
  python main.py
  Select: "Implicit Neural Representations: ..."
  Field: "Neural Network Theory & Coordinate-Based Representations"
  
✓ Configuration:
  ACADEMIC_RIGOR_MODE = True
  RESEARCH_MODE = True
  
✓ Files Generated:
  - debate_*.md (transcript)
  - research_kit_*_foundational_papers.json
  - research_kit_*_verified_claims.json
  - research_kit_*_citation_analysis.json
  - research_kit_*_debate_rigor.json
  - [+ 15 more analyses]
""")

print("=" * 70)
