"""
Phase 5 Results Exporter
Export ICLR readiness analysis to JSON and HTML for sharing/persistence.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import config


def export_phase5_json(
    session_topic: str,
    formal_problems: List[Dict[str, Any]],
    novelty_assessments: List[Dict[str, Any]],
    solution_sketches: List[Dict[str, Any]],
    readiness_scores: List[Dict[str, Any]],
    export_dir: str = None
) -> str:
    """
    Export Phase 5 results to JSON files (one per gap).
    Each file contains all analysis stages for that gap.
    """
    if export_dir is None:
        export_dir = config.PhD_ANALYSIS_DIR
    
    os.makedirs(export_dir, exist_ok=True)
    
    # Create index mapping gap titles to their analysis
    problem_map = {p.get("gap_title"): p for p in formal_problems}
    novelty_map = {n.get("gap_title"): n for n in novelty_assessments}
    sketch_map = {s.get("gap_title"): s for s in solution_sketches}
    readiness_map = {r.get("gap_title"): r for r in readiness_scores}
    
    exported_files = []
    
    for gap_title in problem_map.keys():
        gap_data = {
            "session_topic": session_topic,
            "gap_title": gap_title,
            "exported_at": datetime.now().isoformat(),
            
            "formal_problem": problem_map.get(gap_title, {}),
            "novelty_assessment": novelty_map.get(gap_title, {}),
            "solution_sketch": sketch_map.get(gap_title, {}),
            "readiness_assessment": readiness_map.get(gap_title, {}),
        }
        
        # Slugify filename
        safe_name = gap_title[:40].replace(" ", "_").replace("/", "-")
        filename = os.path.join(export_dir, f"analysis_{safe_name}.json")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(gap_data, f, indent=2, ensure_ascii=False)
            exported_files.append(filename)
        except Exception as e:
            print(f"  Error exporting {gap_title}: {e}")
    
    # Also create summary index file
    summary = {
        "session_topic": session_topic,
        "total_gaps": len(problem_map),
        "formalization_rate": len(problem_map) / max(len(problem_map), 1),
        "novelty_rate": len(novelty_map) / max(len(formal_problems), 1),
        "sketch_rate": len(sketch_map) / max(len(formal_problems), 1),
        "readiness_rate": len(readiness_map) / max(len(formal_problems), 1),
        "top_gap": readiness_scores[0] if readiness_scores else {},
        "exported_files": exported_files,
        "exported_at": datetime.now().isoformat()
    }
    
    index_file = os.path.join(export_dir, f"phase5_index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        exported_files.insert(0, index_file)
    except Exception as e:
        print(f"  Error writing index: {e}")
    
    return export_dir


def _generate_html_header(title: str) -> str:
    """Generate HTML header."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        .content {{
            padding: 3rem;
        }}
        .gap-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 2rem;
            overflow: hidden;
        }}
        .gap-title {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-bottom: 2px solid #667eea;
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
        }}
        .gap-body {{
            padding: 2rem;
        }}
        .section {{
            margin-bottom: 2rem;
        }}
        .section-title {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 1rem;
            border-bottom: 1px solid #ddd;
            padding-bottom: 0.5rem;
        }}
        .score-badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-weight: bold;
            font-size: 1rem;
            margin: 0.25rem;
        }}
        .score-high {{ background: #d4edda; color: #155724; }}
        .score-medium {{ background: #fff3cd; color: #856404; }}
        .score-low {{ background: #f8d7da; color: #721c24; }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .metric-label {{
            font-weight: 500;
            color: #555;
        }}
        .metric-value {{
            color: #667eea;
            font-weight: bold;
        }}
        .action-item {{
            background: #f8f9fa;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        .action-priority {{
            font-weight: bold;
            padding: 0.25rem 0.75rem;
            border-radius: 3px;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }}
        .priority-high {{ background: #f8d7da; color: #721c24; }}
        .priority-medium {{ background: #fff3cd; color: #856404; }}
        .priority-low {{ background: #d4edda; color: #155724; }}
        .footer {{
            background: #f8f9fa;
            padding: 2rem;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ICLR Readiness Assessment</h1>
            <p>{title}</p>
        </div>
        <div class="content">
"""


def _generate_html_footer() -> str:
    """Generate HTML footer."""
    return f"""
        </div>
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>ProfOcto ICLR Readiness Analysis</p>
        </div>
    </div>
</body>
</html>
"""


def export_phase5_html(
    session_topic: str,
    readiness_scores: List[Dict[str, Any]],
    export_dir: str = None
) -> str:
    """
    Generate HTML visualization of readiness assessment results.
    """
    if export_dir is None:
        export_dir = config.PhD_ANALYSIS_DIR
    
    os.makedirs(export_dir, exist_ok=True)
    
    # Start HTML
    html_parts = [_generate_html_header(session_topic)]
    
    # Sort by readiness score descending
    sorted_gaps = sorted(readiness_scores, key=lambda x: x.get("iclr_readiness_score", 0), reverse=True)
    
    for gap in sorted_gaps:
        gap_title = gap.get("gap_title", "Unknown")
        score = gap.get("iclr_readiness_score", 0)
        recommendation = gap.get("recommendation", "Unknown")
        
        # Determine score color
        if score >= 70:
            score_class = "score-high"
        elif score >= 50:
            score_class = "score-medium"
        else:
            score_class = "score-low"
        
        html_parts.append(f"""
            <div class="gap-card">
                <div class="gap-title">{gap_title}</div>
                <div class="gap-body">
                    <div class="section">
                        <div class="section-title">Overall Assessment</div>
                        <div class="metric">
                            <span class="metric-label">ICLR Readiness Score</span>
                            <span class="score-badge {score_class}">{score:.0f}/100</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Recommendation</span>
                            <span class="metric-value">{recommendation}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Confidence</span>
                            <span class="metric-value">{gap.get('recommendation_confidence', 0):.0%}</span>
                        </div>
                    </div>
        """)
        
        # Scoring breakdown
        breakdown = gap.get("scoring_breakdown", {})
        if breakdown:
            html_parts.append("""
                    <div class="section">
                        <div class="section-title">Scoring Breakdown</div>
            """)
            for component, value in breakdown.items():
                if component != "overall_score":
                    html_parts.append(f"""
                        <div class="metric">
                            <span class="metric-label">{component.replace('_', ' ').title()}</span>
                            <span class="metric-value">{value:.0f}/100</span>
                        </div>
                    """)
            html_parts.append("</div>")
        
        # Timeline
        timeline = gap.get("timeline_assessment", {})
        if timeline:
            html_parts.append(f"""
                    <div class="section">
                        <div class="section-title">Timeline Estimate</div>
                        <div class="metric">
                            <span class="metric-label">Total Duration</span>
                            <span class="metric-value">~{timeline.get('total_timeline_months', 0):.0f} months</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Research Phase</span>
                            <span class="metric-value">{timeline.get('research_phase', 'N/A')}</span>
                        </div>
                    </div>
            """)
        
        # Risk assessment
        risk = gap.get("risk_assessment", {})
        if risk:
            risk_level = risk.get("risk_level", "Unknown")
            risk_color = "red" if risk_level == "Very High" else "orange" if risk_level in ["High", "Medium"] else "green"
            html_parts.append(f"""
                    <div class="section">
                        <div class="section-title">Risk Assessment</div>
                        <div class="metric">
                            <span class="metric-label">Overall Risk Level</span>
                            <span class="metric-value" style="color: {risk_color};">{risk_level}</span>
                        </div>
            """)
            risks = risk.get("major_risks", [])
            if risks:
                html_parts.append("<div style='margin-top: 0.75rem;'><strong>Major Risks:</strong>")
                for r in risks[:3]:
                    html_parts.append(f"<p>⚠️ {r}</p>")
                html_parts.append("</div>")
            html_parts.append("</div>")
        
        # Action items
        actions = gap.get("action_items", [])
        if actions:
            html_parts.append("""
                    <div class="section">
                        <div class="section-title">Action Items</div>
            """)
            for item in actions[:5]:
                priority = item.get("priority", "Medium")
                priority_class = f"priority-{priority.lower()}"
                html_parts.append(f"""
                        <div class="action-item">
                            <span class="action-priority {priority_class}">{priority}</span>
                            <strong>{item.get('action', '')}</strong>
                            <br><small>⏱ {item.get('timeline', '')}</small>
                        </div>
                """)
            html_parts.append("</div>")
        
        html_parts.append("</div></div>")  # Close gap-body and gap-card
    
    # Footer
    html_parts.append(_generate_html_footer())
    
    # Write to file
    filename = os.path.join(export_dir, f"phase5_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(html_parts))
    except Exception as e:
        print(f"Error writing HTML report: {e}")
        return None
    
    return filename
