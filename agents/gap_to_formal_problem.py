"""
Gap to Formal Problem Converter

Convert informal research gaps (from debate) → 
Formal mathematical problem statements with theorem definitions.

Maintains full trace back to debate context.
"""

import json
from typing import Dict, List, Any
import config
from utils.logger import get_logger


def _call_gemini_formalize(prompt: str, max_tokens: int = 2000) -> str:
    """Call Gemini to formalize problem."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        logger.log_error("gap_formalizer", ImportError("google-genai not installed"))
        return "{}"
    
    logger.log_api_call("gap_formalizer", config.MODEL, len(prompt))
    
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.5},
        )
        result = response.text.strip()
        logger.log_api_response("gap_formalizer", len(result))
        return result
    except Exception as e:
        logger.log_error("gap_formalizer", e, context="Gemini call failed")
        return "{}"


def formalize_research_gap(
    gap: Dict[str, Any],
    debate_context: Dict[str, Any],
    session_topic: str
) -> Dict[str, Any]:
    """
    Convert informal research gap to formal problem statement.
    
    Parameters:
        gap: Research gap identified from debate
        debate_context: {
            "turns": [{"speaker": str, "role": str, "content": str}],
            "all_professors": [{"name": str, ...}]
        }
        session_topic: Main debate topic
    
    Returns: {
        "gap_id": int,
        "gap_title": str,
        "gap_source": "Debate debate Turn X vs Turn Y",
        "formal_problem": {
            "title": str,
            "definition": str,
            "input_variables": [{"name": str, "description": str, "constraints": str}],
            "objective": str,
            "constraints": [str],
            "definitions": [{"term": str, "definition": str}]
        },
        "theorem_skeleton": {
            "main_theorem": {
                "statement": str,
                "proof_sketch": str,
                "dependencies": [str]  # What lemmas needed
            },
            "required_lemmas": [
                {"name": str, "statement": str, "difficulty": str}
            ]
        },
        "mathematical_framework": str,  # Tools needed
        "complexity_analysis": {
            "current_sota": str,  # From debate
            "target": str,  # What you want to achieve
            "gap": str  # Why there's a gap
        },
        "debate_references": [
            {
                "turn": int,
                "speaker": str,
                "role": str,
                "claim": str,
                "relevance": str
            }
        ],
        "trace_log": str  # How this gap was formalized
    }
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Formalizing gap: {gap.get('title', 'Unknown')}")
    
    try:
        # Build context from debate
        debate_summary = _build_debate_context(debate_context)
        
        formalization_prompt = f"""
You are a mathematical researcher. Your task is to convert an informal research gap 
(identified from academic debate) into a FORMAL problem statement.

DEBATE CONTEXT:
{debate_summary}

SESSION TOPIC: {session_topic}

RESEARCH GAP TO FORMALIZE:
Title: {gap.get('title', 'Unknown')}
Description: {gap.get('description', '')}
Mathematical basis: {gap.get('mathematical_basis', '')}
Type: {gap.get('type', 'unknown')}

Task: Create a FORMAL PROBLEM STATEMENT that:
1. Defines mathematically what the gap is
2. Lists input parameters with constraints
3. States the objective (what you want to achieve)
4. Identifies required theorems/lemmas
5. Proposes solution skeleton

Respond ONLY as JSON (no markdown):

{{
    "formal_problem": {{
        "title": "Formal problem name",
        "definition": "Given [inputs], find [solution] such that [properties]",
        "input_variables": [
            {{
                "name": "n",
                "description": "sequence length",
                "constraints": "positive integer, n < 10^6"
            }}
        ],
        "objective": "Minimize [X] subject to [constraints]",
        "constraints": [
            "Time complexity: o(n²)",
            "Space complexity: O(n)",
            "Approximation error ≤ ε"
        ],
        "definitions": [
            {{
                "term": "Attention matrix",
                "definition": "A = softmax(QK^T / √d) ∈ ℝ^(n×n)"
            }}
        ]
    }},
    "theorem_skeleton": {{
        "main_theorem": {{
            "statement": "For inputs satisfying [conditions], there exists algorithm A with complexity C and accuracy ε",
            "proof_approach": "Use [technique 1], [technique 2], then combine with [theorem X]",
            "dependencies": ["Lemma A", "Lemma B", "Theorem from [Paper]"]
        }},
        "required_lemmas": [
            {{
                "name": "Rank bound",
                "statement": "For [condition], rank(A) ≤ r",
                "difficulty": "moderate",
                "tools": ["spectral analysis", "matrix concentration"]
            }}
        ]
    }},
    "mathematical_framework": "Low-rank approximation, spectral analysis, complexity theory",
    "complexity_analysis": {{
        "sota_best": "O(n²) (standard attention by Vaswani et al.)",
        "sota_alternative": "O(n) with approximation error (Performer)",
        "target_improvement": "O(n√n) with deterministic guarantee",
        "why_gap_exists": "Current methods trade off complexity vs quality; need Pareto improvement"
    }},
    "key_insight": "Brief explanation of proof strategy"
}}
"""
        
        result_json = _call_gemini_formalize(formalization_prompt, max_tokens=2500)
        
        try:
            result = json.loads(result_json)
        except json.JSONDecodeError:
            logger.log_warning("gap_formalizer", f"Invalid JSON for {gap.get('title')}")
            result = {
                "formal_problem": {},
                "theorem_skeleton": {},
                "mathematical_framework": "Unable to formalize",
                "complexity_analysis": {}
            }
        
        # Add debate references + tracing
        full_result = {
            "gap_id": gap.get("gap_id", -1),
            "gap_title": gap.get("title", "Unknown"),
            "gap_type": gap.get("type", "unknown"),
            "gap_source": f"Debate on {session_topic}",
            "debate_references": _trace_debate_references(gap, debate_context),
            "formal_problem": result.get("formal_problem", {}),
            "theorem_skeleton": result.get("theorem_skeleton", {}),
            "mathematical_framework": result.get("mathematical_framework", ""),
            "complexity_analysis": result.get("complexity_analysis", {}),
            "trace_log": _generate_trace_log(gap, result)
        }
        
        logger.gap_logger.info(f"✓ Gap formalized: {gap.get('title')}")
        logger.gap_logger.debug(f"  Framework: {result.get('mathematical_framework', '')}")
        
        return full_result
    
    except Exception as e:
        logger.log_error("gap_formalizer", e, context=f"Failed to formalize gap: {gap.get('title')}")
        return {
            "gap_id": gap.get("gap_id", -1),
            "gap_title": gap.get("title", "Unknown"),
            "formal_problem": {},
            "theorem_skeleton": {},
            "error": str(e)
        }


def _build_debate_context(debate_context: Dict[str, Any]) -> str:
    """Build summary of relevant debate context."""
    
    turns = debate_context.get("turns", [])
    professors = {p.get("name", "Unknown"): p for p in debate_context.get("all_professors", [])}
    
    summary_lines = []
    summary_lines.append("Key debate exchanges:")
    
    # Show last 5 turns (most relevant)
    for turn in turns[-5:]:
        speaker = turn.get("speaker", "Unknown")
        role = turn.get("role", "")
        content = turn.get("content", "")[:200]  # First 200 chars
        summary_lines.append(f"- {speaker} ({role}): {content}...")
    
    return "\n".join(summary_lines)


def _trace_debate_references(gap: Dict[str, Any], debate_context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Trace which debate turns led to this gap identification.
    """
    
    # Simple heuristic: gap involves professors mentioned in affected_professors
    affected = gap.get("affected_professors", [])
    turns = debate_context.get("turns", [])
    
    references = []
    for i, turn in enumerate(turns):
        speaker = turn.get("speaker", "")
        if speaker in affected:
            references.append({
                "turn": i + 1,
                "speaker": speaker,
                "role": turn.get("role", ""),
                "claim_snippet": turn.get("content", "")[:150],
                "relevance": f"Professor {speaker} contributed to this gap"
            })
    
    return references[:3]  # Top 3 references


def _generate_trace_log(gap: Dict[str, Any], formal_result: Dict[str, Any]) -> str:
    """
    Generate trace log showing how informal gap became formal problem.
    """
    
    log = []
    log.append(f"FORMALIZATION TRACE LOG")
    log.append(f"─" * 50)
    log.append(f"Informal gap: {gap.get('title', 'Unknown')}")
    log.append(f"Type: {gap.get('type', 'unknown')}")
    log.append(f"Description: {gap.get('description', '')[:200]}...")
    log.append("")
    log.append(f"Formalized to:")
    log.append(f"Title: {formal_result.get('formal_problem', {}).get('title', 'N/A')}")
    log.append(f"Framework: {formal_result.get('mathematical_framework', 'N/A')}")
    log.append(f"Required lemmas: {len(formal_result.get('theorem_skeleton', {}).get('required_lemmas', []))} lemmas")
    log.append(f"─" * 50)
    
    return "\n".join(log)


def formalize_all_gaps(
    gaps: List[Dict[str, Any]],
    debate_context: Dict[str, Any],
    session_topic: str
) -> List[Dict[str, Any]]:
    """
    Formalize all gaps from a debate session.
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Formalizing {len(gaps)} research gaps")
    
    formalized_gaps = []
    for gap in gaps:
        try:
            formal_gap = formalize_research_gap(gap, debate_context, session_topic)
            formalized_gaps.append(formal_gap)
        except Exception as e:
            logger.gap_logger.warning(f"Failed to formalize {gap.get('title')}: {str(e)}")
    
    logger.gap_logger.info(f"✓ Formalized {len(formalized_gaps)} gaps")
    
    return formalized_gaps
