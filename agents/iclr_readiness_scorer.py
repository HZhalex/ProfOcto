"""
ICLR Readiness Scorer

Assess whether a research gap is ready/viable for PhD pursuit toward ICLR publication.
Combines novelty, feasibility, and debate evidence into actionable recommendation.

Traces all scoring back to debate depth and rigor.
"""

import json
from typing import Dict, List, Any, Tuple
import config
from utils.logger import get_logger


def _call_gemini_assess_readiness(prompt: str, max_tokens: int = 2000) -> str:
    """Call Gemini to assess ICLR readiness."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        logger.log_error("iclr_readiness", ImportError("google-genai not installed"))
        return "{}"
    
    logger.log_api_call("iclr_readiness", config.MODEL, len(prompt))
    
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.3},  # Low temp for consistency
        )
        result = response.text.strip()
        logger.log_api_response("iclr_readiness", len(result))
        return result
    except Exception as e:
        logger.log_error("iclr_readiness", e, context="Gemini call failed")
        return "{}"


def assess_iclr_readiness(
    gap_analysis: Dict[str, Any],
    novelty_analysis: Dict[str, Any],
    solution_sketch: Dict[str, Any],
    session_rigor_scores: List[float]
) -> Dict[str, Any]:
    """
    Comprehensive ICLR readiness assessment.
    
    Parameters:
        gap_analysis: From gap_to_formal_problem.py
        novelty_analysis: From novelty_analyzer.py
        solution_sketch: From solution_sketch.py
        session_rigor_scores: Rigor scores from debate (0-10 scale)
    
    Returns: {
        "gap_title": str,
        "iclr_readiness_score": float,  # 0-100
        "recommendation": str,  # "Pursue", "Promising but risky", "Not ready"
        "recommendation_confidence": float,  # 0-1
        "scoring_breakdown": {
            "novelty_component": float,  # Weighted novelty score
            "feasibility_component": float,  # Time estimate, difficulty
            "evidence_quality": float,  # How well supported by debate
            "advisor_fit": float,  # How well problem suits PhD context
            "overall_score": float
        },
        "timeline_assessment": {
            "research_phase": str,  # "0-3 months", "3-6 months", "6-12 months", "12+ months"
            "publication_phase": str,
            "total_timeline_months": float,
            "critical_path": str
        },
        "risk_assessment": {
            "risk_level": str,  # "Low", "Medium", "High", "Very High"
            "major_risks": [str],
            "risk_mitigation": [{"risk": str, "mitigation": str}]
        },
        "action_items": [
            {
                "priority": "High" | "Medium" | "Low",
                "action": str,
                "timeline": str
            }
        ],
        "debate_evidence_summary": {
            "supporting_arguments": [str],
            "challenging_arguments": [str],
            "evidence_quality_rating": str,  # "Strong", "Moderate", "Weak"
            "debate_depth": str  # How thorough was debate
        },
        "comparison_to_peer_gaps": str,  # If multiple gaps: how does this rank?
        "final_verdict": str,  # Executive summary: pursue or not
        "trace_log": str
    }
    """
    logger = get_logger()
    
    gap_title = gap_analysis.get("gap_title", "Unknown")
    logger.gap_logger.info(f">> Assessing ICLR readiness: {gap_title}")
    
    try:
        # Calculate evidence quality from rigor scores
        avg_rigor = sum(session_rigor_scores) / len(session_rigor_scores) if session_rigor_scores else 0
        evidence_quality = min(1.0, avg_rigor / 10.0)  # 0-10 scale → 0-1
        
        readiness_prompt = f"""
You are an ICLR program chair and PhD advisor. Assess whether a research gap is ready for PhD pursuit.

GAP ANALYSIS:
Title: {gap_title}
Type: {gap_analysis.get('gap_type', 'unknown')}
Framework: {gap_analysis.get('mathematical_framework', '')}

NOVELTY ASSESSMENT:
ICLR Score: {novelty_analysis.get('iclr_score', 0)}/100
Verdict: {novelty_analysis.get('iclr_likelihood', 'Unknown')}
Key improvements: {novelty_analysis.get('improvement_over_sota', '')}

SOLUTION FEASIBILITY:
Difficulty: {solution_sketch.get('estimated_difficulty', 'Unknown')}
Timeline: ~{solution_sketch.get('time_estimate_months', 12)} months (1 student)
Key insight: {solution_sketch.get('proof_strategy', '')[:100]}

DEBATE EVIDENCE QUALITY: {evidence_quality:.1%} 
(Based on mathematical rigor of argument sources)

Task: Provide ICLR readiness assessment that considers:
1. Novelty: Is this novel enough for ICLR? How do competing methods compare?
2. Feasibility: Can 1 PhD student solve this in 6-12 months?
3. Evidence: Is debate support for problem formulation strong?
4. Risk: What could make this fail? (overclaimed results, wrong direction, etc)
5. Timeline: What's realistic for 3-6-12 month milestones?

Respond ONLY as JSON:

{{
    "iclr_readiness_score": 72,
    "recommendation": "Pursue",
    "recommendation_confidence": 0.78,
    "scoring_breakdown": {{
        "novelty_component": 80,
        "feasibility_component": 65,
        "evidence_quality": 75,
        "advisor_fit": 80,
        "overall_score": 72
    }},
    "timeline_assessment": {{
        "research_phase": "3-6 months",
        "publication_phase": "6-9 months",
        "total_timeline_months": 12,
        "critical_path": "Rank estimation algorithm → proof of ε-approximation → experimental validation"
    }},
    "risk_assessment": {{
        "risk_level": "Medium",
        "major_risks": [
            "Constants in O(n√n) might be too large for practical use",
            "Proof technique may not extend to multi-head attention",
            "Competing work on similar ideas may be in progress"
        ],
        "risk_mitigation": [
            {{
                "risk": "Large hidden constants",
                "mitigation": "Plan early experiments on small-medium sequences. May need to combine with other techniques."
            }},
            {{
                "risk": "Generalization limits",
                "mitigation": "Identify theoretical limits early (via negative results). Focus on specific attention patterns."
            }}
        ]
    }},
    "action_items": [
        {{
            "priority": "High",
            "action": "Implement rank estimation algorithm and verify complexity empirically",
            "timeline": "Weeks 1-4"
        }},
        {{
            "priority": "High",
            "action": "Prove main theorem: ε-approximation guarantee for estimated rank",
            "timeline": "Weeks 5-12"
        }},
        {{
            "priority": "Medium",
            "action": "Literature search: check recent ArXiv papers on linear attention",
            "timeline": "Ongoing"
        }}
    ],
    "debate_evidence_summary": {{
        "supporting_arguments": [
            "Spectral decay of attention matrices is well-established (Chen's point)",
            "Sampling-based statistics is mature field (Kumar's references)",
            "O(n) vs O(n²) complexity gap is acknowledged problem (Rodriguez)"
        ],
        "challenging_arguments": [
            "Performer already achieves o(n²) with randomized approach",
            "May require expensive pre-computation vs standard attention"
        ],
        "evidence_quality_rating": "Strong",
        "debate_depth": "Thorough - multiple professors engaged with mathematical details"
    }},
    "comparison_to_peer_gaps": "This gap is more concrete and tractable than alternative gaps, with clearer novelty over Performer.",
    "final_verdict": "RECOMMENDED. Strong novelty signal, feasible timeline, solid debate evidence. Medium risk (hidden constants, generalization) but mitigatable. Pursue with focus on empirical validation early.",
    "overall_recommendation_reasoning": "Gap demonstrates clear complexity improvement over SOTA, backed by rigorous debate. Solution sketch is concrete with ~4-6 month research timeline. Main risk is practical applicability (constants), suggesting monthly empirical milestones."
}}
"""
        
        result_json = _call_gemini_assess_readiness(readiness_prompt, max_tokens=2000)
        
        try:
            result = json.loads(result_json)
        except json.JSONDecodeError:
            logger.gap_logger.warning(f"Invalid JSON for readiness assessment")
            result = {
                "iclr_readiness_score": 0,
                "recommendation": "Unable to assess",
                "recommendation_confidence": 0
            }
        
        # Clamp scores
        result["iclr_readiness_score"] = max(0, min(100, result.get("iclr_readiness_score", 0)))
        result["recommendation_confidence"] = max(0, min(1.0, result.get("recommendation_confidence", 0)))
        
        # Build full result
        full_result = {
            "gap_title": gap_title,
            "iclr_readiness_score": result.get("iclr_readiness_score", 0),
            "recommendation": result.get("recommendation", "Unable to assess"),
            "recommendation_confidence": result.get("recommendation_confidence", 0),
            "scoring_breakdown": result.get("scoring_breakdown", {}),
            "timeline_assessment": result.get("timeline_assessment", {}),
            "risk_assessment": result.get("risk_assessment", {}),
            "action_items": result.get("action_items", []),
            "debate_evidence_summary": result.get("debate_evidence_summary", {}),
            "comparison_to_peer_gaps": result.get("comparison_to_peer_gaps", ""),
            "final_verdict": result.get("final_verdict", ""),
            "trace_log": _generate_readiness_trace(
                gap_analysis, novelty_analysis, solution_sketch, result
            )
        }
        
        logger.gap_logger.info(f"✓ Readiness assessed: {gap_title}")
        logger.gap_logger.info(f"  Score: {result.get('iclr_readiness_score', 0)}/100 | Recommendation: {result.get('recommendation', '?')}")
        
        return full_result
    
    except Exception as e:
        logger.log_error("iclr_readiness", e, context=f"Failed to assess readiness")
        return {
            "gap_title": gap_title,
            "iclr_readiness_score": 0,
            "recommendation": "Assessment failed",
            "recommendation_confidence": 0,
            "error": str(e)
        }


def _generate_readiness_trace(
    gap_analysis: Dict[str, Any],
    novelty_analysis: Dict[str, Any],
    solution_sketch: Dict[str, Any],
    readiness_result: Dict[str, Any]
) -> str:
    """Generate comprehensive readiness assessment trace."""
    
    log = []
    log.append("ICLR READINESS ASSESSMENT TRACE")
    log.append("=" * 60)
    log.append(f"Gap: {gap_analysis.get('gap_title', 'Unknown')}")
    log.append("")
    
    # Scoring breakdown
    log.append("SCORING COMPONENTS:")
    breakdown = readiness_result.get("scoring_breakdown", {})
    log.append(f"  Novelty:         {breakdown.get('novelty_component', 0):.0f}/100")
    log.append(f"  Feasibility:     {breakdown.get('feasibility_component', 0):.0f}/100")
    log.append(f"  Evidence quality: {breakdown.get('evidence_quality', 0):.0f}/100")
    log.append(f"  Advisor fit:     {breakdown.get('advisor_fit', 0):.0f}/100")
    log.append(f"  ──────────────────────")
    log.append(f"  OVERALL:         {readiness_result.get('iclr_readiness_score', 0):.0f}/100")
    log.append("")
    
    # Timeline
    log.append("TIMELINE:")
    timeline = readiness_result.get("timeline_assessment", {})
    log.append(f"  Research:     {timeline.get('research_phase', '?')}")
    log.append(f"  Publication:  {timeline.get('publication_phase', '?')}")
    log.append(f"  Total:        ~{timeline.get('total_timeline_months', 0):.0f} months")
    log.append("")
    
    # Recommendation
    log.append("RECOMMENDATION:")
    log.append(f"  {readiness_result.get('recommendation', '?')} (confidence: {readiness_result.get('recommendation_confidence', 0):.0%})")
    log.append("")
    
    # Risk assessment
    risk = readiness_result.get("risk_assessment", {})
    if risk:
        log.append(f"RISK LEVEL: {risk.get('risk_level', 'Unknown')}")
        risks = risk.get('major_risks', [])
        if risks:
            log.append("  Major risks:")
            for r in risks[:3]:
                log.append(f"    ⚠ {r}")
    log.append("")
    
    # Action items
    actions = readiness_result.get("action_items", [])
    if actions:
        log.append("ACTION ITEMS:")
        for item in actions[:5]:
            log.append(f"  [{item.get('priority', '?')}] {item.get('action', '')}")
            log.append(f"      Timeline: {item.get('timeline', '?')}")
    
    log.append("=" * 60)
    
    return "\n".join(log)


def assess_batch(
    gap_analyses: List[Dict[str, Any]],
    novelty_analyses: List[Dict[str, Any]],
    solution_sketches: List[Dict[str, Any]],
    session_rigor_scores: List[float]
) -> List[Dict[str, Any]]:
    """
    Assess ICLR readiness for multiple gaps.
    """
    logger = get_logger()
    
    logger.gap_logger.info(f">> Assessing ICLR readiness for {len(gap_analyses)} gaps")
    
    readiness_scores = []
    
    # Match gaps to novelty and sketch analyses
    gap_map = {g.get("gap_title"): g for g in gap_analyses}
    novelty_map = {n.get("gap_title"): n for n in novelty_analyses}
    sketch_map = {s.get("gap_title"): s for s in solution_sketches}
    
    for gap in gap_analyses:
        title = gap.get("gap_title", "Unknown")
        try:
            novelty = novelty_map.get(title, {})
            sketch = sketch_map.get(title, {})
            
            assessment = assess_iclr_readiness(gap, novelty, sketch, session_rigor_scores)
            readiness_scores.append(assessment)
        except Exception as e:
            logger.gap_logger.warning(f"Failed to assess {title}: {str(e)}")
    
    # Sort by readiness score (highest first)
    readiness_scores.sort(key=lambda x: x.get("iclr_readiness_score", 0), reverse=True)
    
    logger.gap_logger.info(f"✓ Assessed readiness for {len(readiness_scores)} gaps")
    
    return readiness_scores


def score_recommendation(readiness_result: Dict[str, Any]) -> Tuple[int, str]:
    """
    Convert recommendation to priority score.
    
    Returns: (score, label)
        score: 1=Pursue (priority), 2=Promising, 3=Risky, 4=Not ready
        label: Human-readable version
    """
    recommendation = readiness_result.get("recommendation", "Unknown").lower()
    
    if "pursue" in recommendation or "recommended" in recommendation:
        priority = 1
        label = "🎯 Pursue"
    elif "promising" in recommendation:
        priority = 2
        label = "⚡ Promising but risky"
    elif "risky" in recommendation or "not ready" in recommendation:
        priority = 3
        label = "⚠️ High risk"
    else:
        priority = 4
        label = "❌ Not ready"
    
    return priority, label


def format_executive_summary(readiness_results: List[Dict[str, Any]], top_n: int = 3) -> str:
    """
    Format executive summary of top gaps for PhD pursuit.
    """
    lines = []
    lines.append("ICLR READINESS - TOP RESEARCH GAPS")
    lines.append("=" * 60)
    lines.append("")
    
    sorted_results = sorted(
        readiness_results,
        key=lambda x: x.get("iclr_readiness_score", 0),
        reverse=True
    )
    
    for i, result in enumerate(sorted_results[:top_n], 1):
        priority, label = score_recommendation(result)
        
        lines.append(f"{i}. {result.get('gap_title', 'Unknown')}")
        lines.append(f"   {label}")
        lines.append(f"   ICLR Score: {result.get('iclr_readiness_score', 0):.0f}/100 (confidence: {result.get('recommendation_confidence', 0):.0%})")
        
        timeline = result.get("timeline_assessment", {})
        lines.append(f"   Timeline: ~{timeline.get('total_timeline_months', 0):.0f} months")
        
        risk = result.get("risk_assessment", {})
        lines.append(f"   Risk: {risk.get('risk_level', 'Unknown')}")
        
        verdict = result.get("final_verdict", "").split(".")[0]  # First sentence
        if verdict:
            lines.append(f"   → {verdict[:80]}...")
        
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)
