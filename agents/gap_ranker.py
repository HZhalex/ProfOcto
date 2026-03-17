"""
Gap Comparison & Ranking Tool
Compare multiple research gaps side-by-side with different ranking strategies.
Help PhD students choose between gaps based on their constraints/preferences.
"""

from typing import Dict, List, Any, Tuple
from utils.logger import get_logger


def score_gap_for_criteria(
    gap: Dict[str, Any],
    criteria: str = "balanced"
) -> float:
    """
    Score a gap based on different prioritization criteria.
    
    criteria:
        - "novelty": Maximize ICLR novelty (ignores feasibility)
        - "feasibility": Minimize effort/time (ignores impact)
        - "balanced": Pareto-optimal (innovation vs effort)
        - "impact": Maximize expected impact (novelty + advisor fit)
        - "speed": Maximize speed to first result (easy to start & sustain)
    """
    novelty = gap.get("novelty_assessment", {}).get("iclr_score", 0)
    readiness = gap.get("readiness_assessment", {})
    feasibility_comp = readiness.get("scoring_breakdown", {}).get("feasibility_component", 50)
    timeline = readiness.get("timeline_assessment", {}).get("total_timeline_months", 12)
    confidence = readiness.get("recommendation_confidence", 0.5)
    risk_level = readiness.get("risk_assessment", {}).get("risk_level", "Medium")
    
    risk_score = {"Low": 100, "Medium": 75, "High": 50, "Very High": 25}.get(risk_level, 50)
    
    if criteria == "novelty":
        return novelty
    elif criteria == "feasibility":
        return feasibility_comp / max(timeline, 1)  # Feasibility / months
    elif criteria == "balanced":
        # Pareto score: maximize both, weighted equally
        return (novelty * 0.4 + feasibility_comp * 0.3 + risk_score * 0.2 + (confidence * 100) * 0.1)
    elif criteria == "impact":
        advisor_fit = readiness.get("scoring_breakdown", {}).get("advisor_fit", 50)
        return (novelty * 0.5 + advisor_fit * 0.3 + feasibility_comp * 0.2)
    elif criteria == "speed":
        speed_score = max(0, 100 - timeline * 5)  # Penalty: 5 points per month
        return (feasibility_comp * 0.5 + speed_score * 0.5)
    
    return readiness.get("iclr_readiness_score", 0)


def rank_gaps(
    readiness_scores: List[Dict[str, Any]],
    criteria: str = "balanced"
) -> List[Tuple[str, float, int]]:
    """
    Rank gaps by specified criteria.
    
    Returns: [(gap_title, score, rank), ...]
    """
    logger = get_logger()
    
    logger.gap_logger.info(f"Ranking {len(readiness_scores)} gaps by '{criteria}' criteria")
    
    gap_scores = [
        (gap.get("gap_title", "Unknown"), score_gap_for_criteria({"novelty_assessment": {}, "readiness_assessment": gap}, criteria))
        for gap in readiness_scores
    ]
    
    # Sort by score descending
    gap_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Add rank
    ranked = [(title, score, rank + 1) for rank, (title, score) in enumerate(gap_scores)]
    
    return ranked


def generate_comparison_table(
    readiness_scores: List[Dict[str, Any]]
) -> str:
    """
    Generate ASCII table comparing all gaps across key metrics.
    """
    logger = get_logger()
    
    if not readiness_scores:
        return "No gaps to compare."
    
    # Prepare data
    rows = []
    for gap in sorted(readiness_scores, key=lambda x: x.get("iclr_readiness_score", 0), reverse=True):
        title = gap.get("gap_title", "Unknown")[:30]
        readiness = gap.get("iclr_readiness_score", 0)
        novelty = gap.get("novelty_assessment", {}).get("iclr_score", 0) if "novelty_assessment" in gap else 0
        timeline = gap.get("timeline_assessment", {}).get("total_timeline_months", 0)
        risk = gap.get("risk_assessment", {}).get("risk_level", "?")[0]
        recommendation = gap.get("recommendation", "?")[0]
        
        rows.append({
            "Gap": title,
            "Readiness": f"{readiness:.0f}",
            "Novelty": f"{novelty:.0f}",
            "Timeline(mo)": f"{timeline:.0f}",
            "Risk": risk,
            "Rec": recommendation
        })
    
    # Format as ASCII table
    if not rows:
        return "No data."
    
    headers = list(rows[0].keys())
    col_widths = {h: max(len(h), max((len(str(r[h])) for r in rows), default=5)) for h in headers}
    
    # Build table
    lines = []
    sep = " | ".join("─" * col_widths[h] for h in headers)
    lines.append(" | ".join(f"{h:<{col_widths[h]}}" for h in headers))
    lines.append(sep)
    
    for row in rows:
        lines.append(" | ".join(f"{str(row[h]):<{col_widths[h]}}" for h in headers))
    
    return "\n".join(lines)


def identify_pareto_frontier(
    readiness_scores: List[Dict[str, Any]]
) -> List[str]:
    """
    Identify Pareto-optimal gaps (Pareto frontier).
    A gap is Pareto-optimal if no other gap dominates it on all dimensions.
    
    Dimensions: (novelty, feasibility, confidence, risk)
    """
    logger = get_logger()
    
    if not readiness_scores:
        return []
    
    # Extract metrics
    gaps_with_metrics = []
    for gap in readiness_scores:
        novelty = gap.get("novelty_assessment", {}).get("iclr_score", 0) if "novelty_assessment" in gap else gap.get("iclr_readiness_score", 0)
        feasibility = gap.get("scoring_breakdown", {}).get("feasibility_component", 50)
        confidence = gap.get("recommendation_confidence", 0.5)
        risk_level = gap.get("risk_assessment", {}).get("risk_level", "Medium")
        risk_score = {"Low": 4, "Medium": 3, "High": 2, "Very High": 1}.get(risk_level, 2)
        
        gaps_with_metrics.append({
            "title": gap.get("gap_title", "Unknown"),
            "novelty": novelty,
            "feasibility": feasibility,
            "confidence": confidence,
            "risk": risk_score
        })
    
    # Find Pareto frontier
    frontier = []
    for gap in gaps_with_metrics:
        is_dominated = False
        for other in gaps_with_metrics:
            if other["title"] == gap["title"]:
                continue
            
            # Check if 'other' dominates 'gap'
            if (other["novelty"] >= gap["novelty"] and
                other["feasibility"] >= gap["feasibility"] and
                other["confidence"] >= gap["confidence"] and
                other["risk"] >= gap["risk"]):
                
                # Strict domination requires at least one strict inequality
                if (other["novelty"] > gap["novelty"] or
                    other["feasibility"] > gap["feasibility"] or
                    other["confidence"] > gap["confidence"] or
                    other["risk"] > gap["risk"]):
                    is_dominated = True
                    break
        
        if not is_dominated:
            frontier.append(gap["title"])
    
    logger.gap_logger.info(f"Pareto frontier: {len(frontier)} gaps out of {len(gaps_with_metrics)}")
    return frontier


def recommend_based_on_constraints(
    readiness_scores: List[Dict[str, Any]],
    constraints: Dict[str, Any]
) -> List[Tuple[str, float, str]]:
    """
    Recommend gaps based on user constraints.
    
    constraints: {
        "max_timeline_months": 12,
        "min_novelty": 60,
        "max_risk": "High",  # Accept up to this risk
        "advisor_availability": "full" | "part",
    }
    """
    logger = get_logger()
    
    max_timeline = constraints.get("max_timeline_months", 24)
    min_novelty = constraints.get("min_novelty", 0)
    max_risk_level = constraints.get("max_risk", "Very High")
    advisor_availability = constraints.get("advisor_availability", "full")
    
    risk_hierarchy = {"Low": 1, "Medium": 2, "High": 3, "Very High": 4}
    max_risk_score = risk_hierarchy.get(max_risk_level, 4)
    
    candidates = []
    for gap in readiness_scores:
        novelty = gap.get("novelty_assessment", {}).get("iclr_score", 0) if "novelty_assessment" in gap else gap.get("iclr_readiness_score", 0)
        timeline = gap.get("timeline_assessment", {}).get("total_timeline_months", 100)
        risk = gap.get("risk_assessment", {}).get("risk_level", "Very High")
        risk_score = risk_hierarchy.get(risk, 4)
        
        # Check constraints
        if novelty < min_novelty:
            continue
        if timeline > max_timeline:
            continue
        if risk_score > max_risk_score:
            continue
        
        # Score based on constraints
        score = (novelty * 0.5 + (100 - timeline * 2) * 0.3 + (50 / risk_score) * 0.2)
        
        candidates.append((gap.get("gap_title", "Unknown"), score, "FEASIBLE"))
    
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    logger.gap_logger.info(f"Found {len(candidates)} feasible gaps matching constraints")
    
    return candidates


def analyze_gap_portfolio(
    readiness_scores: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Analyze the overall portfolio of gaps.
    Useful for understanding coverage and balance.
    """
    logger = get_logger()
    
    if not readiness_scores:
        return {}
    
    # Statistics
    novelties = []
    timelines = []
    risks = []
    
    for gap in readiness_scores:
        novelty = gap.get("novelty_assessment", {}).get("iclr_score", 0) if "novelty_assessment" in gap else gap.get("iclr_readiness_score", 0)
        timeline = gap.get("timeline_assessment", {}).get("total_timeline_months", 0)
        risk = gap.get("risk_assessment", {}).get("risk_level", "Medium")
        
        novelties.append(novelty)
        timelines.append(timeline)
        risks.append(risk)
    
    avg_novelty = sum(novelties) / len(novelties) if novelties else 0
    avg_timeline = sum(timelines) / len(timelines) if timelines else 0
    
    risk_counts = {}
    for r in risks:
        risk_counts[r] = risk_counts.get(r, 0) + 1
    
    analysis = {
        "total_gaps": len(readiness_scores),
        "average_novelty": avg_novelty,
        "novelty_range": (min(novelties), max(novelties)) if novelties else (0, 0),
        "average_timeline_months": avg_timeline,
        "timeline_range": (min(timelines), max(timelines)) if timelines else (0, 0),
        "risk_distribution": risk_counts,
        "recommended_portfolio": {
            "high_impact": [g["gap_title"] for g in readiness_scores if g.get("novelty_assessment", {}).get("iclr_score", 0) > avg_novelty + 10][:2],
            "quick_wins": [g["gap_title"] for g in readiness_scores if g.get("timeline_assessment", {}).get("total_timeline_months", 0) < avg_timeline - 3][:2],
        }
    }
    
    logger.gap_logger.info(f"Portfolio analysis: avg novelty {avg_novelty:.0f}, avg timeline {avg_timeline:.0f} months")
    
    return analysis
