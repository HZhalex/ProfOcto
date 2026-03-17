#!/usr/bin/env python3
"""
Example: How to Use Advanced Research Mode for PhD Research

This shows how to run the Academic Debate Arena with advanced research synthesis
for your PhD dissertation at Stanford.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config

# IMPORTANT: Advanced research mode is enabled in config.py
print(f"Research Mode: {config.RESEARCH_MODE}")

# Example 1: Run via command line
print("\n" + "="*70)
print("EXAMPLE 1: Command Line Usage")
print("="*70)
print("""
# For LLMs/AI research:
python main.py \\
  "Emergent abilities in LLMs: why scaling causes capability jumps" \\
  "AI/Large Language Models"

# For distributed systems:
python main.py \\
  "Tensor Parallelism vs Pipeline Parallelism vs MoE: optimal strategy?" \\
  "Distributed Machine Learning"

# For vision:
python main.py \\
  "Vision Transformers vs CNNs: when/why win transformers?" \\
  "Computer Vision"
""")

# Example 2: Interpret the output files
print("\n" + "="*70)
print("EXAMPLE 2: Understanding Output Files")
print("="*70)
print("""
After running a debate, check these files in research_kits/:

1. research_kit_[topic]_research_gaps.json
   → What hasn't been studied yet
   → Gold mine for PhD topic selection
   
2. research_kit_[topic]_novel_approaches.json
   → New ways to solve the problem
   → Potential methodology for your work
   
3. research_kit_[topic]_breakthrough_areas.json
   → WHERE YOU CAN HAVE MAXIMUM IMPACT
   → Read this first to position your research
   
4. research_kit_[topic]_theoretical_foundations.json
   → What theories apply + what's missing
   → Grounding for your dissertation argument
   
5. research_kit_[topic]_methodology_innovations.json
   → How to validate in novel ways
   → Your experimental design inspiration
   
6. research_kit_[topic]_cross_domain_insights.json
   → Ideas from Physics, Bio, Economics, etc.
   → Revolutionary combinations
   
7. research_kit_[topic]_counterarguments.json
   → Strongest criticisms to address
   → Strengthen your work by defending against these
""")

# Example 3: Workflow for dissertation planning
print("\n" + "="*70)
print("EXAMPLE 3: Dissertation Planning Workflow")
print("="*70)
print("""
WEEK 1: Choose broad research area
  → Run debate on general topic
  → Read: research_gaps.json, counterarguments.json
  → Get: Initial sense of landscape

WEEK 2-3: Identify positioning
  → Read: breakthrough_areas.json
  → Read: novel_approaches.json
  → Ask: Where can I have outsized impact?
  → Ask: What's genuinely new about my approach?

WEEK 4-5: Design methodology
  → Read: methodology_innovations.json
  → Read: theoretical_foundations.json
  → Design: Novel experimental approach
  → Ground: In solid theory + address identified gaps

WEEK 6+: Build dissertation
  → Outline: Use outline.md as starting point
  → Motivation: Combine research_gaps + breakthrough_areas
  → Literature: Use key_findings + cross_domain_insights
  → Methods: Use methodology_innovations perspective
  → Limitations: Directly from counterarguments.json
  → Contribution: Clear from positioning in breakthrough_areas
""")

# Example 4: Configuration
print("\n" + "="*70)
print("EXAMPLE 4: Configuration Options (config.py)")
print("="*70)
print("""
# Enable/disable research mode
RESEARCH_MODE = True  # Set to False to skip research synthesis

# Model settings
MODEL = "gemma-3-1b-it"  # Or upgrade to "gemini-2.0", "claude-3.5"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # Set in .env

# Debate settings
NUM_PROFESSORS = 2    # 2-5 professors (more = deeper debate)
MAX_TURNS_PER_ROUND = 1
MAX_ROUNDS = 2        # More rounds = more thorough analysis

# Research settings
RESEARCH_KIT_DIR = "research_kits"
RESEARCH_MAX_RECOMMENDATIONS = 5
""")

# Example 5: Advanced usage
print("\n" + "="*70)
print("EXAMPLE 5: Advanced Tips")
print("="*70)
print("""
MULTIPLE DEBATES ON SAME TOPIC:
  → Run 3 debates with different professor configurations
  → Combine insights across all runs
  → Get more comprehensive picture

USE SPECIFIC TOPICS:
  ✗ "Machine Learning" (too vague)
  ✓ "Scaling Laws in Transformers: Chinchilla Token Allocation" (specific)

CUSTOMIZE PROFESSOR PROFILES:
  → Edit orchestrator.py _pick_universities() to add domain-specific professors
  → Add specific experts for your field

ITERATE:
  → Start broad, then narrow down
  → Each debate informs next debate
  → After 3-5 iterations, clear dissertation area emerges

CROSS-REFER OUTPUTS:
  → See gap in research_gaps.json?
  → Check if addressed in novel_approaches.json
  → See if it appears in counterarguments.json
  → Validates the gap's importance
""")

# Example 6: Expected output
print("\n" + "="*70)
print("EXAMPLE 6: What Good Results Look Like")
print("="*70)
print("""
GOOD research_gaps.json:
  - 5-7 distinct gaps
  - Specific (not vague)
  - Varied difficulty levels
  - Clear impact statement
  
GOOD breakthrough_areas.json:
  - 4-6 areas
  - Each with clear potential impact
  - Feasible for PhD (not 10-year project)
  - Different angles on same problem
  
GOOD novel_approaches.json:
  - 3-5 approaches
  - Distinctly different from each other
  - Technically sound but under-explored
  - Clear "why not done yet?" explanation
  
GOOD counterarguments.json:
  - Strongest criticisms identified
  - Hidden assumptions surfaced
  - Edge cases that break current approaches
  - Empirical challenges clearly stated
""")

# Example 7: Next steps
print("\n" + "="*70)
print("EXAMPLE 7: After Running Debates")
print("="*70)
print("""
IMMEDIATE (Day 1):
  1. Read all JSON files (especially breakthrough_areas.json)
  2. Write 1-2 page summary of findings
  3. Identify 3 most interesting breakthrough areas

SHORT-TERM (Week 1-2):
  4. Deep dive into chosen areas
  5. Search literature for "gap" + "area combinations
  6. Sketch research design for top 3 ideas
  7. Discuss with advisor/lab

MEDIUM-TERM (Week 3-4):
  8. Run MORE debates on narrower topics
  9. Develop detailed research proposal
  10. Set up experiments/implementation

LONG-TERM (Month 2+):
  11. Use counterarguments.json to defend approach
  12. Reference cross_domain_insights in your writing
  13. Ground in theoretical_foundations.json
  14. Validate with methodology_innovations.json
""")

print("\n" + "="*70)
print("Ready to revolutionize your field? 🚀")
print("="*70)
print("""
This system is designed to:
  ✅ Accelerate topic selection (weeks → days)
  ✅ Identify genuine research gaps
  ✅ Find where YOU can have breakthrough impact
  ✅ Design novel methodologies
  ✅ Give cross-disciplinary perspectives
  ✅ Strengthen your work against criticism

Good luck with your Stanford PhD research!
""")
