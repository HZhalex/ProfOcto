"""
Research Gap Identifier for PhD Students

Detect gaps from:
- Mathematical contradictions
- Assumption violations
- Efficiency-quality trade-offs
- Unanswered questions

WITH COMPREHENSIVE LOGGING & ERROR HANDLING
"""

import json
from typing import Dict, List, Any
from agents.theorem_extractor import analyze_mathematical_consistency
import config
from utils.logger import get_logger


def _call_gemini_gap_analysis(prompt: str, max_tokens: int = 2000) -> str:
    """Call Gemini for gap analysis with error handling."""
    logger = get_logger()
    
    try:
        from google import genai
    except ImportError:
        logger.log_error("gap_identifier", ImportError("google-genai not installed"))
        return "{}"
    
    logger.log_api_call("gap_identifier", config.MODEL, len(prompt))
    
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens, "temperature": 0.4},
        )
        result = response.text.strip()
        logger.log_api_response("gap_identifier", len(result))
        return result
    except Exception as e:
        logger.log_error("gap_identifier", e, context="Gemini API call failed for gap analysis")
        return "{}"


def identify_research_gaps(
    all_turns: List[Dict[str, Any]],
    topic: str
) -> List[Dict[str, Any]]:
    """
    Identify research gaps from debate.
    
    Args:
        all_turns: List of {speaker, theorems_data, content}
        topic: Debate topic
    
    Returns:
        List of research gaps ranked by PhD value
    """
    logger = get_logger()
    logger.log_gap_detection_start(len(all_turns))
    
    try:
        all_theorems = {}
        for turn in all_turns:
            speaker = turn.get("speaker", "Unknown")
            theorems = turn.get("theorems_data", {})
            all_theorems[speaker] = theorems
        
        # Find contradictions
        contradictions = _find_mathematical_contradictions(all_theorems)
        
        # Find assumption violations
        assumption_gaps = _find_assumption_violations(all_turns)
        
        # Find trade-off gaps
        tradeoff_gaps = _find_tradeoff_gaps(all_theorems)
        
        # Find unanswered questions
        unanswered_gaps = _find_unanswered_questions(all_turns, topic)
        
        # Combine and rank
        all_gaps = contradictions + assumption_gaps + tradeoff_gaps + unanswered_gaps
        all_gaps = sorted(all_gaps, key=lambda x: _score_phd_value(x), reverse=True)
        
        logger.log_gap_detection_complete(len(all_gaps))
        
        return all_gaps[:10]
    
    except Exception as e:
        logger.log_gap_detection_error(e)
        return []


def _find_mathematical_contradictions(all_theorems: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Find direct math contradictions between professors."""
    logger = get_logger()
    gaps = []
    speakers = list(all_theorems.keys())
    
    logger.gap_logger.debug(f"Analyzing {len(speakers)} professors for contradictions")
    
    for i, speaker1 in enumerate(speakers):
        for speaker2 in speakers[i+1:]:
            try:
                consistency = analyze_mathematical_consistency(
                    all_theorems[speaker1],
                    all_theorems[speaker2]
                )
                
                for contradiction in consistency.get("contradictions", []):
                    gap = {
                        "gap_id": len(gaps),
                        "type": "theoretical_contradiction",
                        "title": _synthesize_contradiction_title(contradiction),
                        "description": f"{speaker1} vs {speaker2}",
                        "mathematical_basis": contradiction.get("research_gap", ""),
                        "related_theorems": [],
                        "affected_professors": [speaker1, speaker2],
                        "difficulty": "PhD",
                        "potential_approaches": [],
                        "phd_value": "High",
                        "industry_impact": "Critical",
                    }
                    gaps.append(gap)
                    logger.log_gap_detected(gap["gap_id"], gap["type"], gap["title"], gap["difficulty"], gap["phd_value"])
            
            except Exception as e:
                logger.gap_logger.warning(f"Error comparing {speaker1} vs {speaker2}: {str(e)}")
    
    return gaps


def _synthesize_contradiction_title(contradiction: Dict[str, str]) -> str:
    """Generate readable gap title."""
    nature = contradiction.get("nature", "unknown")
    
    if "complexity" in contradiction.get("prof1_claim", "").lower():
        return "Complexity Bound Discrepancy"
    elif "assumption" in nature:
        return "Conflicting Assumptions"
    else:
        return "Theoretical Conflict"


def _find_assumption_violations(all_turns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find assumption violations."""
    logger = get_logger()
    gaps = []
    
    logger.gap_logger.debug(f"Checking {len(all_turns)} turns for assumption violations")
    
    for turn in all_turns:
        try:
            theorems_data = turn.get("theorems_data", {})
            content = turn.get("content", "")
            speaker = turn.get("speaker", "Unknown")
            
            for assumption in theorems_data.get("assumptions", []):
                if assumption.get("critical", False):
                    if any(word in content.lower() for word in ["violate", "invalid", "fail", "cannot", "impractical"]):
                        gap = {
                            "gap_id": len(gaps),
                            "type": "assumption_violation",
                            "title": f"Assumption Violation",
                            "description": assumption.get("assumption", ""),
                            "mathematical_basis": assumption.get("context", ""),
                            "related_theorems": [],
                            "affected_professors": [speaker],
                            "difficulty": "Master",
                            "potential_approaches": [],
                            "phd_value": "Medium",
                            "industry_impact": "High",
                        }
                        gaps.append(gap)
                        logger.log_gap_detected(gap["gap_id"], gap["type"], gap["title"], gap["difficulty"], gap["phd_value"])
        
        except Exception as e:
            logger.gap_logger.warning(f"Error analyzing assumptions for {turn.get('speaker', 'Unknown')}: {str(e)}")
    
    return gaps


def _find_tradeoff_gaps(all_theorems: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Find efficiency-quality trade-offs."""
    logger = get_logger()
    gaps = []
    
    if len(all_theorems) >= 2:
        gap = {
            "gap_id": 0,
            "type": "pareto_frontier",
            "title": "Efficiency-Quality Trade-off",
            "description": "No algorithm dominates others",
            "mathematical_basis": "Pareto optimization problem",
            "related_theorems": [],
            "affected_professors": list(all_theorems.keys()),
            "difficulty": "PhD",
            "potential_approaches": [],
            "phd_value": "High",
            "industry_impact": "Critical",
        }
        gaps.append(gap)
        logger.log_gap_detected(gap["gap_id"], gap["type"], gap["title"], gap["difficulty"], gap["phd_value"])
    
    return gaps


def _find_unanswered_questions(all_turns: List[Dict[str, Any]], topic: str) -> List[Dict[str, Any]]:
    """Find unresolved questions."""
    logger = get_logger()
    
    try:
        gap_detection_prompt = f"""
Topic: {topic}

Identify key unresolved research questions from debate. Respond as JSON only.

{{
    "unanswered_gaps": [
        {{"question": "What is ...?", "why_important": "Because ...", "difficulty": "PhD"}}
    ]
}}
"""
        
        result_json = _call_gemini_gap_analysis(gap_detection_prompt)
        
        try:
            result = json.loads(result_json)
            gaps = []
            for i, unanswered in enumerate(result.get("unanswered_gaps", [])):
                gap = {
                    "gap_id": i,
                    "type": "unanswered_question",
                    "title": unanswered.get("question", "Unknown"),
                    "description": unanswered.get("why_important", ""),
                    "mathematical_basis": "",
                    "related_theorems": [],
                    "affected_professors": [],
                    "difficulty": unanswered.get("difficulty", "PhD"),
                    "potential_approaches": [],
                    "phd_value": "High",
                    "industry_impact": None,
                }
                gaps.append(gap)
                logger.log_gap_detected(gap["gap_id"], gap["type"], gap["title"], gap["difficulty"], gap["phd_value"])
            return gaps
        except json.JSONDecodeError:
            logger.log_warning("gap_identifier", "Invalid JSON in unanswered questions")
            return []
    
    except Exception as e:
        logger.log_error("gap_identifier", e, context="Unanswered questions detection failed")
        return []


def _score_phd_value(gap: Dict[str, Any]) -> float:
    """Score PhD publication potential."""
    score = 0.0
    
    if gap.get("difficulty") == "PhD":
        score += 2.0
    elif gap.get("difficulty") == "Master":
        score += 1.0
    
    if gap.get("phd_value") == "High":
        score += 3.0
    elif gap.get("phd_value") == "Medium":
        score += 1.5
    
    if gap.get("industry_impact"):
        score += 1.0
    
    return score


def generate_phd_research_recommendations(gaps: List[Dict[str, Any]]) -> str:
    """Convert gaps to PhD research recommendations."""
    logger = get_logger()
    logger.gap_logger.info(f"Generating PhD recommendations from {len(gaps)} gaps")
    
    if not gaps:
        return "No research gaps identified."
    
    recommendations = "# PHD RESEARCH RECOMMENDATIONS\n\n"
    
    try:
        for i, gap in enumerate(gaps[:5], 1):
            recommendations += f"## {i}. {gap['title']}\n"
            recommendations += f"**Difficulty**: {gap.get('difficulty', 'Unknown')}\n"
            recommendations += f"**PhD Value**: {gap.get('phd_value', 'Unknown')}\n"
            recommendations += f"**Mathematical Basis**: {gap.get('mathematical_basis', '')}\n\n"
            if gap.get('industry_impact'):
                recommendations += f"**Industry Impact**: {gap['industry_impact']}\n\n"
        
        logger.gap_logger.info("PhD recommendations generated successfully")
    
    except Exception as e:
        logger.log_error("gap_identifier", e, context="Failed to generate recommendations")
    
    return recommendations
