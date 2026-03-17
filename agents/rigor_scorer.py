"""
Mathematical Rigor Scorer

Score each turn on math backing (0-10):
- Theorem citations (35%)
- Proof density (30%)
- Citation quality (20%)
- Logical consistency (15%)

WITH COMPREHENSIVE LOGGING
"""

import json
from typing import Dict, List, Any
from agents.theorem_extractor import extract_theorems, extract_citations
import config
from utils.logger import get_logger


def score_mathematical_rigor(
    content: str,
    speaker_name: str,
    speaker_profiles: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Score turn by mathematical rigor with detailed logging."""
    logger = get_logger()
    logger.log_rigor_scoring_start(speaker_name)
    
    try:
        # Extract data
        theorems_data = extract_theorems(content, speaker_name)
        citations = extract_citations(content)
        
        # Score components
        theorem_score = _score_theorem_citations(theorems_data)
        proof_score = _score_proof_density(theorems_data, content)
        citation_score = _score_citation_quality(citations)
        consistency_score = _score_logical_consistency(theorems_data)
        
        # Total (weighted)
        total_score = (
            theorem_score * 0.35 +
            proof_score * 0.30 +
            citation_score * 0.20 +
            consistency_score * 0.15
        )
        
        # Verdict
        if total_score >= 8.5:
            verdict = "HIGHLY_RIGOROUS"
        elif total_score >= 7:
            verdict = "RIGOROUS"
        elif total_score >= 5:
            verdict = "MODERATELY_BACKED"
        elif total_score >= 3:
            verdict = "OPINION_BASED"
        else:
            verdict = "UNSUPPORTED"
        
        strengths, weaknesses = _analyze_strengths_weaknesses(
            theorems_data, citations, total_score
        )
        
        breakdown = {
            "theorem_citation_score": theorem_score,
            "proof_density_score": proof_score,
            "citation_quality_score": citation_score,
            "logical_consistency_score": consistency_score,
        }
        
        result = {
            "speaker": speaker_name,
            "turn_content_length": len(content),
            "rigor_score": round(total_score, 2),
            "breakdown": breakdown,
            "details": {
                "num_theorems_cited": len(theorems_data.get("theorems", [])),
                "num_papers_cited": len(citations),
                "proof_coverage": theorems_data.get("math_density", 0.0),
                "rigor_level": theorems_data.get("rigor_level", "informal"),
            },
            "verdict": verdict,
            "key_strengths": strengths,
            "weaknesses": weaknesses,
        }
        
        logger.log_rigor_scoring_result(speaker_name, total_score, verdict, breakdown)
        return result
    
    except Exception as e:
        logger.log_rigor_scoring_error(speaker_name, e)
        return {
            "speaker": speaker_name,
            "rigor_score": 0.0,
            "verdict": "ERROR",
            "breakdown": {},
            "details": {},
            "key_strengths": [],
            "weaknesses": ["Error during scoring"],
        }


def _score_theorem_citations(theorems_data: Dict[str, Any]) -> float:
    """Score based on theorems cited."""
    num_theorems = len(theorems_data.get("theorems", []))
    
    if num_theorems == 0:
        return 0.0
    elif num_theorems <= 2:
        score = 1.5
    elif num_theorems <= 5:
        score = 2.2
    else:
        score = 3.0
    
    major_types = sum(1 for t in theorems_data.get("theorems", [])
                      if t.get("type") in ["architecture", "optimization"])
    if major_types >= 2:
        score = min(3.0, score + 0.3)
    
    return score


def _score_proof_density(theorems_data: Dict[str, Any], content: str) -> float:
    """Score based on proof density & math statements."""
    math_density = theorems_data.get("math_density", 0.0)
    
    if math_density < 0.2:
        score = 0.5
    elif math_density < 0.4:
        score = 1.2
    elif math_density < 0.6:
        score = 2.0
    else:
        score = 3.0
    
    num_proofs = len(theorems_data.get("proofs_or_sketch", []))
    if num_proofs >= 2:
        score = min(3.0, score + 0.5)
    
    return score


def _score_citation_quality(citations: List[Dict[str, str]]) -> float:
    """Score citation quality."""
    if not citations:
        return 0.0
    
    foundational_authors = {"vaswani", "hinton", "lecun", "bengio", "transformer"}
    score = 0.0
    top_tier_count = 0
    
    for cite in citations:
        authors = cite.get("authors", "").lower()
        
        if any(founder in authors for founder in foundational_authors):
            if top_tier_count < 2:
                score += 0.4
                top_tier_count += 1
        elif top_tier_count < 2:
            score += 0.2
            top_tier_count += 1
        elif len(citations) > 4:
            score += 0.1
    
    return min(2.0, score)


def _score_logical_consistency(theorems_data: Dict[str, Any]) -> float:
    """Score logical consistency."""
    score = 0.0
    
    if len(theorems_data.get("proofs_or_sketch", [])) > 0:
        score += 1.5
    
    if len(theorems_data.get("assumptions", [])) > 0:
        score += 0.3
    
    score += 0.2
    
    return min(2.0, score)


def _analyze_strengths_weaknesses(
    theorems_data: Dict[str, Any],
    citations: List[Dict[str, str]],
    total_score: float
) -> tuple[List[str], List[str]]:
    """Generate strengths & weaknesses."""
    
    strengths = []
    weaknesses = []
    
    if len(theorems_data.get("theorems", [])) >= 3:
        strengths.append("Strong theoretical foundation")
    
    if theorems_data.get("math_density", 0.0) >= 0.5:
        strengths.append("High proof density")
    
    if len(citations) >= 5:
        strengths.append("Solid citation base")
    
    if theorems_data.get("rigor_level") in ["rigorous", "highly_rigorous"]:
        strengths.append("Rigorous mathematical standard")
    
    if len(theorems_data.get("theorems", [])) == 0:
        weaknesses.append("No formal theorem citations")
    
    if theorems_data.get("math_density", 0.0) < 0.3:
        weaknesses.append("Limited mathematical backing")
    
    if len(citations) == 0:
        weaknesses.append("Claims lack citation support")
    
    if theorems_data.get("rigor_level") == "informal":
        weaknesses.append("Informal without proofs")
    
    return strengths[:3], weaknesses[:3]


def compare_rigor(score_1: Dict[str, Any], score_2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare rigor scores of 2 professors."""
    logger = get_logger()
    
    diff = score_1["rigor_score"] - score_2["rigor_score"]
    winner = score_1["speaker"] if diff > 0 else score_2["speaker"]
    
    logger.rigor_logger.info(f"Comparison: {score_1['speaker']} ({score_1['rigor_score']}) vs {score_2['speaker']} ({score_2['rigor_score']})")
    
    return {
        "speaker_1": score_1["speaker"],
        "score_1": score_1["rigor_score"],
        "verdict_1": score_1["verdict"],
        
        "speaker_2": score_2["speaker"],
        "score_2": score_2["rigor_score"],
        "verdict_2": score_2["verdict"],
        
        "difference": round(abs(diff), 2),
        "winner_by_rigor": winner if abs(diff) > 0.5 else "Comparable rigor",
    }
