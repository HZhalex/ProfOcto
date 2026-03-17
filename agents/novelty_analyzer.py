"""
Novelty Analyzer

Assess novelty of research gap against state-of-the-art papers.
Score for ICLR suitability based on debate context.

Maintains complete trace back to cited papers and professor arguments.
"""

import json
from typing import Dict, List, Any
import config
from utils.logger import get_logger


def _call_gemini_analyze_novelty(prompt: str, max_tokens: int = 2000) -> str:
    """Call Gemini to analyze novelty."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        logger.log_error("novelty_analyzer", ImportError("google-genai not installed"))
        return "{}"
    
    logger.log_api_call("novelty_analyzer", config.MODEL, len(prompt))
    
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.3},  # Lower temp for consistency
        )
        result = response.text.strip()
        logger.log_api_response("novelty_analyzer", len(result))
        return result
    except Exception as e:
        logger.log_error("novelty_analyzer", e, context="Gemini call failed")
        return "{}"


def score_novelty(
    formal_problem: Dict[str, Any],
    session_citations: List[Dict[str, Any]],
    debate_context: Dict[str, Any],
    session_topic: str
) -> Dict[str, Any]:
    """
    Analyze novelty of formal problem against SOTA papers.
    
    Parameters:
        formal_problem: From gap_to_formal_problem.py
        session_citations: All citations extracted from debate
        debate_context: Full debate turns and professors
        session_topic: Main research topic
    
    Returns: {
        "gap_title": str,
        "novelty_score": float,  # 0-100 (ICLR suitability)
        "novelty_verdict": str,  # "Novel for ICLR", "Borderline", "Not novel"
        "novelty_reasoning": str,
        "iclr_score": float,  # 0-100
        "iclr_likelihood": str,  # "High", "Medium", "Low"
        "comparison_to_sota": [
            {
                "paper": str,
                "year": int,
                "novelty_vs_this": str,  # "Builds on", "Extends", "Contradicts", "Independent"
                "contribution": str,
                "cited_in_debate": str,  # Which professor cited this
                "debate_context": str  # Why cited it
            }
        ],
        "improvement_over_sota": {
            "complexity_improvement": str,  # "O(n^2) → O(n log n)"
            "quality_improvement": str,  # "Approximation factor"
            "generality_improvement": str  # What's new in scope
        },
        "research_gaps_addressed": [str],  # Which gaps this solves
        "potential_blockers": [str],  # Issues that could reduce novelty
        "confidence": float,  # 0-1
        "trace_log": str
    }
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Analyzing novelty of: {formal_problem.get('gap_title', 'Unknown')}")
    
    try:
        # Build citation context from debate
        citation_context = _build_citation_context(session_citations, debate_context)
        
        novelty_prompt = f"""
You are an ICLR area chair. Your task is to assess the NOVELTY of a research problem 
against state-of-the-art papers cited in academic debate.

SESSION TOPIC: {session_topic}

PAPERS CITED IN DEBATE:
{citation_context}

FORMAL PROBLEM TO ASSESS:
Title: {formal_problem.get('formal_problem', {}).get('title', 'Unknown')}
Definition: {formal_problem.get('formal_problem', {}).get('definition', '')}
Framework: {formal_problem.get('mathematical_framework', '')}
Complexity gap: {formal_problem.get('complexity_analysis', {}).get('gap', '')}
Target improvement: {formal_problem.get('complexity_analysis', {}).get('target_improvement', '')}

Task: Assess novelty for ICLR publication (top-tier venue).

Respond ONLY as JSON:

{{
    "novelty_score": 75,
    "novelty_verdict": "Novel for ICLR",
    "novelty_reasoning": "Clear contribution beyond cited methods. Addresses known complexity gap with new technique.",
    "iclr_score": 72,
    "iclr_likelihood": "High",
    "comparison_to_sota": [
        {{
            "paper": "Attention is All You Need",
            "year": 2017,
            "novelty_vs_this": "Extends from standard attention",
            "contribution": "Improves complexity from O(n²) to O(n log n)",
            "relative_novelty": "medium"
        }},
        {{
            "paper": "Performer",
            "year": 2020,
            "novelty_vs_this": "Builds on random features approach",
            "contribution": "Different approximation strategy",
            "relative_novelty": "moderate"
        }}
    ],
    "improvement_over_sota": {{
        "complexity_improvement": "O(n²) → O(n log n log(1/ε))",
        "quality_improvement": "Deterministic approximation vs probabilistic",
        "generality_improvement": "Works for arbitrary kernels, not just softmax"
    }},
    "research_gaps_addressed": [
        "Quadratic complexity of attention",
        "Approximation quality under memory constraints"
    ],
    "potential_blockers": [
        "Large constants may hide in O(n log n)",
        "Requires strong assumptions on kernel structure"
    ],
    "confidence": 0.78
}}
"""
        
        result_json = _call_gemini_analyze_novelty(novelty_prompt, max_tokens=2000)
        
        try:
            result = json.loads(result_json)
        except json.JSONDecodeError:
            logger.gap_logger.warning(f"Invalid JSON for novelty analysis")
            result = {
                "novelty_score": 0,
                "novelty_verdict": "Unable to assess",
                "iclr_score": 0
            }
        
        # Clamp scores to 0-100
        result["novelty_score"] = max(0, min(100, result.get("novelty_score", 0)))
        result["iclr_score"] = max(0, min(100, result.get("iclr_score", 0)))
        result["confidence"] = max(0, min(1.0, result.get("confidence", 0.5)))
        
        # Build full result with debate tracing
        full_result = {
            "gap_title": formal_problem.get("gap_title", "Unknown"),
            "novelty_score": result.get("novelty_score", 0),
            "novelty_verdict": result.get("novelty_verdict", "Unable to assess"),
            "novelty_reasoning": result.get("novelty_reasoning", ""),
            "iclr_score": result.get("iclr_score", 0),
            "iclr_likelihood": result.get("iclr_likelihood", "Low"),
            "comparison_to_sota": result.get("comparison_to_sota", []),
            "improvement_over_sota": result.get("improvement_over_sota", {}),
            "research_gaps_addressed": result.get("research_gaps_addressed", []),
            "potential_blockers": result.get("potential_blockers", []),
            "confidence": result.get("confidence", 0.5),
            "debate_cited_papers": [c.get("paper", "") for c in session_citations if c.get("paper")],
            "trace_log": _generate_novelty_trace(formal_problem, result)
        }
        
        logger.gap_logger.info(f"✓ Novelty analyzed: {formal_problem.get('gap_title')}")
        logger.gap_logger.info(f"  ICLR Score: {result.get('iclr_score', 0)}/100 ({result.get('iclr_likelihood')})")
        
        return full_result
    
    except Exception as e:
        logger.log_error("novelty_analyzer", e, context=f"Failed to analyze novelty")
        return {
            "gap_title": formal_problem.get("gap_title", "Unknown"),
            "novelty_score": 0,
            "iclr_score": 0,
            "novelty_verdict": "Analysis failed",
            "error": str(e)
        }


def _build_citation_context(session_citations: List[Dict[str, Any]], debate_context: Dict[str, Any]) -> str:
    """Build summary of papers cited in debate."""
    
    if not session_citations:
        return "No papers cited in debate."
    
    lines = []
    for i, citation in enumerate(session_citations[:10], 1):  # Top 10 citations
        paper = citation.get("paper", "Unknown")
        year = citation.get("year", "Unknown")
        relevance = citation.get("relevance", "")
        cited_by = citation.get("cited_by_professor", "Unknown professor")
        
        lines.append(f"{i}. {paper} ({year})")
        lines.append(f"   Cited by: {cited_by}")
        if relevance:
            lines.append(f"   Relevance: {relevance[:100]}")
        lines.append("")
    
    return "\n".join(lines)


def _generate_novelty_trace(formal_problem: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """Generate trace showing how novelty was assessed."""
    
    log = []
    log.append("NOVELTY ASSESSMENT TRACE")
    log.append("─" * 50)
    log.append(f"Problem: {formal_problem.get('gap_title', 'Unknown')}")
    log.append(f"Framework: {formal_problem.get('mathematical_framework', '')}")
    log.append("")
    log.append(f"NOVELTY VERDICT: {analysis.get('novelty_verdict', 'N/A')}")
    log.append(f"ICLR Score: {analysis.get('iclr_score', 0)}/100 → {analysis.get('iclr_likelihood', 'Unknown')}")
    log.append(f"Confidence: {analysis.get('confidence', 0):.1%}")
    log.append("")
    log.append("Improvements over SOTA:")
    improvements = analysis.get('improvement_over_sota', {})
    if improvements:
        log.append(f"  • Complexity: {improvements.get('complexity_improvement', 'N/A')}")
        log.append(f"  • Quality: {improvements.get('quality_improvement', 'N/A')}")
        log.append(f"  • Generality: {improvements.get('generality_improvement', 'N/A')}")
    log.append("")
    
    blockers = analysis.get('potential_blockers', [])
    if blockers:
        log.append("Potential blockers:")
        for blocker in blockers[:3]:
            log.append(f"  ⚠ {blocker}")
    log.append("─" * 50)
    
    return "\n".join(log)


def analyze_novelty_batch(
    formal_problems: List[Dict[str, Any]],
    session_citations: List[Dict[str, Any]],
    debate_context: Dict[str, Any],
    session_topic: str
) -> List[Dict[str, Any]]:
    """
    Analyze novelty of multiple problems.
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Analyzing novelty of {len(formal_problems)} problems")
    
    novelty_results = []
    for problem in formal_problems:
        try:
            result = score_novelty(problem, session_citations, debate_context, session_topic)
            novelty_results.append(result)
        except Exception as e:
            logger.gap_logger.warning(f"Failed to analyze {problem.get('gap_title')}: {str(e)}")
    
    # Sort by novelty score descending
    novelty_results.sort(key=lambda x: x.get("iclr_score", 0), reverse=True)
    
    logger.gap_logger.info(f"✓ Analyzed {len(novelty_results)} problems")
    
    return novelty_results


def filter_iclr_promising(novelty_results: List[Dict[str, Any]], threshold: float = 60.0) -> List[Dict[str, Any]]:
    """
    Filter problems with ICLR likelihood considered 'promising' (score >= threshold).
    """
    promising = [r for r in novelty_results if r.get("iclr_score", 0) >= threshold]
    return promising
