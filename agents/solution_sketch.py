"""
Solution Sketch Generator

Generate proof strategies and solution sketches for research gaps.
Synthesize arguments from professors in the debate.

Maintains full trace showing which professor arguments inspired which parts of solution.
"""

import json
from typing import Dict, List, Any
import config
from utils.logger import get_logger


def _call_gemini_sketch_solution(prompt: str, max_tokens: int = 3000) -> str:
    """Call Gemini to sketch solution."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        logger.log_error("solution_sketch", ImportError("google-genai not installed"))
        return "{}"
    
    logger.log_api_call("solution_sketch", config.MODEL, len(prompt))
    
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.4},
        )
        result = response.text.strip()
        logger.log_api_response("solution_sketch", len(result))
        return result
    except Exception as e:
        logger.log_error("solution_sketch", e, context="Gemini call failed")
        return "{}"


def generate_solution_sketch(
    formal_problem: Dict[str, Any],
    debate_context: Dict[str, Any],
    professor_arguments: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate solution sketch by synthesizing professor arguments.
    
    Parameters:
        formal_problem: From gap_to_formal_problem.py
        debate_context: {
            "turns": [{"speaker": str, "role": str, "content": str}],
            "all_professors": [...]
        }
        professor_arguments: Specific claims made by professors
    
    Returns: {
        "gap_title": str,
        "solution_title": str,
        "proof_strategy": str,  # High-level approach
        "main_theorem": {
            "statement": str,
            "proof_approach": str,
            "complexity": {
                "time": str,  # O(n log n)
                "space": str,
                "general_form": str  # For analysis
            }
        },
        "solution_outline": {
            "phases": [
                {
                    "phase_number": 1,
                    "name": str,
                    "objective": str,
                    "key_steps": [str],
                    "lemmas_used": [str],
                    "mathematical_tools": [str]
                }
            ]
        },
        "proof_sketch": {
            "overview": str,
            "key_lemmas": [
                {
                    "lemma": str,
                    "statement": str,
                    "why_needed": str,
                    "inspired_by": str  # Which professor argument
                }
            ],
            "combining_strategy": str
        },
        "inspired_by_debate": [
            {
                "professor": str,
                "turn": int,
                "argument": str,
                "how_used": str  # How this argument informed solution
            }
        ],
        "critical_insights": [str],  # Breakthroughs from debate
        "open_questions": [str],  # What still needs research
        "estimated_difficulty": str,  # "Easy", "Medium", "Hard", "Very Hard"
        "time_estimate_months": float,  # Rough 1PhD-student-equivalent effort
        "trace_log": str
    }
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Generating solution sketch for: {formal_problem.get('gap_title')}")
    
    try:
        # Build context of professor arguments
        argument_summary = _summarize_professor_arguments(professor_arguments, debate_context)
        
        sketch_prompt = f"""
You are a PhD advisor helping a student develop a solution strategy for a research problem
based on arguments from academic debate between experts.

FORMAL PROBLEM:
Title: {formal_problem.get('formal_problem', {}).get('title', 'Unknown')}
Definition: {formal_problem.get('formal_problem', {}).get('definition', '')}
Theorem skeleton: {formal_problem.get('theorem_skeleton', {}).get('main_theorem', {}).get('statement', '')}
Required framework: {formal_problem.get('mathematical_framework', '')}

PROFESSOR ARGUMENTS THAT CAN INFORM SOLUTION:
{argument_summary}

Task: Create a SOLUTION SKETCH that:
1. Proposes proof strategy synthesizing professor arguments
2. Defines main theorem and required lemmas
3. Breaks down solution into phases
4. Shows how each professor argument contributes
5. Estimates difficulty and timeline

Format response ONLY as JSON:

{{
    "solution_title": "Efficient Attention with Dynamic Rank Approximation",
    "proof_strategy": "Decompose attention into low-rank and residual components. Show residual is O(ε) via matrix perturbation. Combine results via [Theorem X].",
    "main_theorem": {{
        "statement": "For attention matrix A ∈ ℝ^(n×n) with bounded singular values, algorithm Algo achieves O(n√n) time, O(n) space, and ε-multiplication approximation.",
        "proof_approach": "Use matrix concentration bounds to show rank-r approximation, then apply fast SVD. Combine with attention kernel properties.",
        "complexity": {{
            "time": "O(n√n log(1/ε))",
            "space": "O(n log n)",
            "general_form": "Time linear in sequence length times polylog, space linear with log factors"
        }}
    }},
    "solution_outline": {{
        "phases": [
            {{
                "phase_number": 1,
                "name": "Rank estimation phase",
                "objective": "Estimate effective rank of attention matrix",
                "key_steps": [
                    "Sample O(√n log n) random rows",
                    "Estimate spectrum via row sampling",
                    "Determine truncation rank r such that σ_r ≥ ε·σ_1"
                ],
                "lemmas_used": ["Matrix Chernoff bound", "Rank-revealing QR decomposition"],
                "mathematical_tools": ["Random sampling", "Spectral analysis", "Chernoff bounds"]
            }},
            {{
                "phase_number": 2,
                "name": "Low-rank approximation",
                "objective": "Compute rank-r approximation efficiently",
                "key_steps": [
                    "Use fast SVD on sampled rows",
                    "Extend U, V to full column space via sketching",
                    "Compute U·Σ·V^T"
                ],
                "lemmas_used": ["Fast SVD from sketches", "Extension lemma"],
                "mathematical_tools": ["Sketching", "Fast SVD", "Extension technique"]
            }}
        ]
    }},
    "proof_sketch": {{
        "overview": "Show that algorithm achieves ε-approximation in subquadratic time via (1) rank estimation to handle spectrum decay (2) fast approximation via sketching (3) perturbation analysis for error bounds.",
        "key_lemmas": [
            {{
                "lemma": "Rank-r approximation error",
                "statement": "If A = U_r Σ_r V_r^T + E where E has bounded norm, then ||A - U_r Σ_r V_r^T|| ≤ σ_(r+1)",
                "why_needed": "Justifies truncation",
                "inspired_by": "Professor Chen's point about spectral decay"
            }},
            {{
                "lemma": "Fast SVD from samples",
                "statement": "O(√n) row samples suffice to build rank-r SVD with relative error ε",
                "why_needed": "Achieves subquadratic complexity",
                "inspired_by": "Professor Kumar's argument for sampling-based approaches"
            }}
        ],
        "combining_strategy": "Compose lemmas: estimate rank via sampling (Lemma 2) → compute low-rank via fast SVD (Lemma 1) → use perturbation bounds to translate matrix error to attention approximation error (standard analysis) → achieve O(n√n) complexity"
    }},
    "inspired_by_debate": [
        {{
            "professor": "Chen",
            "turn": 3,
            "argument": "Attention matrices typically have decaying singular values",
            "how_used": "Justifies low-rank approximation strategy; rank r << n"
        }},
        {{
            "professor": "Kumar",
            "turn": 5,
            "argument": "Random sampling can estimate singular vectors efficiently",
            "how_used": "Core technique for rank estimation phase in O(√n log n) time"
        }},
        {{
            "professor": "Rodriguez",
            "turn": 7,
            "argument": "Need to handle worst-case approximation guarantees, not just average",
            "how_used": "Motivated requiring deterministic ε-approximation bound, not probabilistic"
        }}
    ],
    "critical_insights": [
        "Key insight: Spectral decay of attention matrices enables low-rank approximation without loss of quality",
        "Sampling-based rank estimation avoids computing full SVD, breaking quadratic barrier",
        "Deterministic guarantees (vs probabilistic) require matrix concentration tools"
    ],
    "open_questions": [
        "Can we improve complexity to O(n) with tighter rank bounds?",
        "Do existing approximation ratios (e.g., from Performer) achieve our ε-guarantee?",
        "How do results extend to multi-head attention?"
    ],
    "estimated_difficulty": "Hard",
    "time_estimate_months": 4
}}
"""
        
        result_json = _call_gemini_sketch_solution(sketch_prompt, max_tokens=3000)
        
        try:
            result = json.loads(result_json)
        except json.JSONDecodeError:
            logger.gap_logger.warning(f"Invalid JSON for solution sketch")
            result = {
                "solution_title": "Solution sketch generation failed",
                "proof_strategy": "",
                "estimated_difficulty": "Unknown"
            }
        
        # Normalize time estimate
        try:
            time_est = float(result.get("time_estimate_months", 6))
            result["time_estimate_months"] = max(0.5, min(24, time_est))  # Clamp 0.5-24 months
        except (TypeError, ValueError):
            result["time_estimate_months"] = 6
        
        # Build full result with debate tracing
        full_result = {
            "gap_title": formal_problem.get("gap_title", "Unknown"),
            "solution_title": result.get("solution_title", "Solution sketch"),
            "proof_strategy": result.get("proof_strategy", ""),
            "main_theorem": result.get("main_theorem", {}),
            "solution_outline": result.get("solution_outline", {}).get("phases", []),
            "proof_sketch": result.get("proof_sketch", {}),
            "inspired_by_debate": result.get("inspired_by_debate", []),
            "critical_insights": result.get("critical_insights", []),
            "open_questions": result.get("open_questions", []),
            "estimated_difficulty": result.get("estimated_difficulty", "Unknown"),
            "time_estimate_months": result.get("time_estimate_months", 6),
            "trace_log": _generate_sketch_trace(formal_problem, result)
        }
        
        logger.gap_logger.info(f"✓ Solution sketch generated: {formal_problem.get('gap_title')}")
        logger.gap_logger.info(f"  Difficulty: {result.get('estimated_difficulty')} | Timeline: ~{result.get('time_estimate_months', 6):.0f} months")
        
        return full_result
    
    except Exception as e:
        logger.log_error("solution_sketch", e, context=f"Failed to generate sketch")
        return {
            "gap_title": formal_problem.get("gap_title", "Unknown"),
            "solution_title": "Generation failed",
            "estimated_difficulty": "Unknown",
            "time_estimate_months": 0,
            "error": str(e)
        }


def _summarize_professor_arguments(
    professor_arguments: List[Dict[str, Any]],
    debate_context: Dict[str, Any]
) -> str:
    """Build summary of relevant professor arguments."""
    
    if not professor_arguments:
        return "No specific arguments provided."
    
    lines = []
    lines.append("Key arguments from debate:")
    
    for i, arg in enumerate(professor_arguments[:8], 1):  # Top 8
        professor = arg.get("professor", "Unknown")
        argument = arg.get("argument", "")
        support = arg.get("mathematical_support", "")
        
        lines.append(f"\n{i}. {professor}:")
        lines.append(f"   Claim: {argument}")
        if support:
            lines.append(f"   Support: {support[:100]}")
    
    return "\n".join(lines)


def _generate_sketch_trace(formal_problem: Dict[str, Any], sketch: Dict[str, Any]) -> str:
    """Generate trace showing how solution was sketched."""
    
    log = []
    log.append("SOLUTION SKETCH GENERATION TRACE")
    log.append("─" * 50)
    log.append(f"Problem: {formal_problem.get('gap_title', 'Unknown')}")
    log.append(f"Mathematical framework: {formal_problem.get('mathematical_framework', '')}")
    log.append("")
    log.append(f"Solution: {sketch.get('solution_title', 'N/A')}")
    log.append(f"Difficulty: {sketch.get('estimated_difficulty', 'Unknown')}")
    log.append(f"Time estimate: ~{sketch.get('time_estimate_months', 0):.0f} months (1 PhD student)")
    log.append("")
    log.append("Main theorem:")
    main_th = sketch.get('main_theorem', {})
    if main_th:
        log.append(f"  {main_th.get('statement', 'N/A')[:100]}...")
        complexity = main_th.get('complexity', {})
        if complexity:
            log.append(f"  Time: {complexity.get('time', 'N/A')}")
            log.append(f"  Space: {complexity.get('space', 'N/A')}")
    log.append("")
    
    phases = sketch.get('solution_outline', [])
    if phases:
        log.append(f"Solution phases: {len(phases)} phases")
        for phase in phases[:3]:
            log.append(f"  • Phase {phase.get('phase_number')}: {phase.get('name')}")
    
    log.append("")
    log.append("Inspired by professor arguments:")
    for arg in sketch.get('inspired_by_debate', [])[:3]:
        log.append(f"  • {arg.get('professor')}: {arg.get('how_used', '')[:50]}...")
    log.append("─" * 50)
    
    return "\n".join(log)


def generate_sketches_batch(
    formal_problems: List[Dict[str, Any]],
    debate_context: Dict[str, Any],
    all_professor_arguments: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate solution sketches for multiple problems.
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Generating solution sketches for {len(formal_problems)} problems")
    
    sketches = []
    for problem in formal_problems:
        try:
            sketch = generate_solution_sketch(problem, debate_context, all_professor_arguments)
            sketches.append(sketch)
        except Exception as e:
            logger.gap_logger.warning(f"Failed to sketch {problem.get('gap_title')}: {str(e)}")
    
    logger.gap_logger.info(f"✓ Generated {len(sketches)} solution sketches")
    
    return sketches


def rank_by_feasibility(sketches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank sketches by feasibility (time estimate and difficulty).
    """
    # Lower time estimate + lower difficulty = better feasibility
    difficulty_scores = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3,
        "Very Hard": 4
    }
    
    def feasibility_score(sketch):
        time = sketch.get("time_estimate_months", 12)
        diff = difficulty_scores.get(sketch.get("estimated_difficulty", "Hard"), 3)
        return time * diff  # Lower is better
    
    return sorted(sketches, key=feasibility_score)
