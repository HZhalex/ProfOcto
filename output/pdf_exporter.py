"""
PDF/Document Exporter for Advisor Sharing
Export gap analysis to shareable formats (PDF, text, HTML).
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List
import config
from utils.logger import get_logger


class AdvisorExporter:
    """Export gap analyses for sharing with advisors."""
    
    def __init__(self, export_dir: str = None):
        self.export_dir = export_dir or config.ADVISOR_EXPORT_DIR
        os.makedirs(self.export_dir, exist_ok=True)
        self.logger = get_logger()
    
    def export_gap_analysis(self, gap_data: Dict[str, Any], format: str = "txt") -> str:
        """
        Export a single gap analysis.
        
        Args:
            gap_data: Gap analysis from Phase 5 readiness scoring
            format: 'txt', 'json', or 'html'
            
        Returns:
            Path to exported file
        """
        if not config.ENABLE_PDF_EXPORT:
            return ""
        
        gap_title = gap_data.get("gap_title", "Unknown Gap")
        filename = self._sanitize_filename(gap_title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "txt":
            filepath = os.path.join(self.export_dir, f"{filename}_{timestamp}.txt")
            content = self._format_as_text(gap_data)
        elif format == "json":
            filepath = os.path.join(self.export_dir, f"{filename}_{timestamp}.json")
            content = json.dumps(gap_data, indent=2, ensure_ascii=False)
        elif format == "html":
            filepath = os.path.join(self.export_dir, f"{filename}_{timestamp}.html")
            content = self._format_as_html(gap_data)
        else:
            return ""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.gap_logger.info(f"Exported gap to {filepath}")
            return filepath
        except Exception as e:
            self.logger.log_error("advisor_export", e, context=f"Failed to export {gap_title}")
            return ""
    
    def export_multiple_gaps(self, gaps: List[Dict[str, Any]], format: str = "txt") -> List[str]:
        """Export multiple gaps."""
        filepaths = []
        for gap in gaps:
            filepath = self.export_gap_analysis(gap, format)
            if filepath:
                filepaths.append(filepath)
        
        # Also create index file
        self._create_index(gaps, format)
        
        return filepaths
    
    def export_run_summary(self, topic: str, gaps: List[Dict[str, Any]], format: str = "txt") -> str:
        """Export summary of entire debate run."""
        if not config.ENABLE_PDF_EXPORT:
            return ""
        
        filename = self._sanitize_filename(f"Summary_{topic}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "txt":
            filepath = os.path.join(self.export_dir, f"{filename}_{timestamp}.txt")
            content = self._format_summary_text(topic, gaps)
        elif format == "html":
            filepath = os.path.join(self.export_dir, f"{filename}_{timestamp}.html")
            content = self._format_summary_html(topic, gaps)
        elif format == "json":
            filepath = os.path.join(self.export_dir, f"{filename}_{timestamp}.json")
            content = json.dumps({
                "topic": topic,
                "exported_at": datetime.now().isoformat(),
                "num_gaps": len(gaps),
                "gaps": gaps
            }, indent=2, ensure_ascii=False)
        else:
            return ""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.gap_logger.info(f"Exported run summary to {filepath}")
            return filepath
        except Exception as e:
            self.logger.log_error("advisor_export", e, context=f"Failed to export run summary for {topic}")
            return ""
    
    def _format_as_text(self, gap_data: Dict[str, Any]) -> str:
        """Format gap analysis as readable text."""
        text = f"""
{'='*70}
RESEARCH GAP ANALYSIS FOR ADVISOR
{'='*70}

Gap Title: {gap_data.get('gap_title', 'Unknown')}
Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'─'*70}
READINESS ASSESSMENT
{'─'*70}
ICLR Readiness Score: {gap_data.get('iclr_readiness_score', 0)}/100
Recommendation: {gap_data.get('recommendation', 'N/A')}

Novelty Score: {gap_data.get('novelty_score', 0)}/100
Feasibility Score: {gap_data.get('feasibility_assessment', {}).get('feasibility_score', 0)}/100

{'─'*70}
PROBLEM STATEMENT
{'─'*70}
{gap_data.get('problem_statement', 'N/A')}

{'─'*70}
KEY INNOVATIONS
{'─'*70}
"""
        for i, innovation in enumerate(gap_data.get('key_innovations', []), 1):
            text += f"{i}. {innovation}\n"
        
        text += f"""
{'─'*70}
TIMELINE ASSESSMENT
{'─'*70}
"""
        timeline = gap_data.get('timeline_assessment', {})
        text += f"""Literature Review: {timeline.get('literature_review_weeks', 0)} weeks
Problem Formalization: {timeline.get('problem_formalization_weeks', 0)} weeks
Solution Development: {timeline.get('solution_development_months', 0)} months
Experimentation: {timeline.get('experimentation_months', 0)} months
Paper Writing: {timeline.get('paper_writing_weeks', 0)} weeks
Total Timeline: {timeline.get('total_timeline_months', 0)} months

{'─'*70}
KEY RISKS AND MITIGATION
{'─'*70}
"""
        
        for i, risk in enumerate(gap_data.get('key_risks', []), 1):
            text += f"{i}. {risk}\n"
        
        text += f"""
{'─'*70}
NEXT STEPS FOR RESEARCHER
{'─'*70}
"""
        for i, step in enumerate(gap_data.get('next_steps_for_researcher', []), 1):
            text += f"{i}. {step}\n"
        
        text += f"""
{'─'*70}
REQUIRED RESOURCES
{'─'*70}
"""
        for i, resource in enumerate(gap_data.get('required_resources', []), 1):
            text += f"{i}. {resource}\n"
        
        text += f"""
{'─'*70}
CONTACT & ADVISOR NOTES
{'─'*70}
Ready for discussion with advisor.
Original analysis date: {datetime.now().isoformat()}

"""
        return text
    
    def _format_as_html(self, gap_data: Dict[str, Any]) -> str:
        """Format gap analysis as HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Gap Analysis - {gap_data.get('gap_title', 'Unknown')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .score {{ font-size: 24px; font-weight: bold; color: #27ae60; }}
        .subsection {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #bdc3c7; }}
        th {{ background: #3498db; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .recommendation {{ background: #d5f4e6; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .footer {{ margin-top: 30px; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>Research Gap Analysis</h1>
    <p><strong>Gap:</strong> {gap_data.get('gap_title', 'Unknown')}</p>
    <p><strong>Exported:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>Readiness Assessment</h2>
    <div class="subsection">
        <p>ICLR Readiness: <span class="score">{gap_data.get('iclr_readiness_score', 0)}/100</span></p>
        <p>Novelty: {gap_data.get('novelty_score', 0)}/100</p>
        <p>Feasibility: {gap_data.get('feasibility_assessment', {}).get('feasibility_score', 0)}/100</p>
    </div>
    
    <div class="recommendation">
        <strong>Recommendation:</strong> {gap_data.get('recommendation', 'N/A')}
    </div>
    
    <h2>Problem Statement</h2>
    <div class="subsection">
        {gap_data.get('problem_statement', 'N/A')}
    </div>
    
    <h2>Key Innovations</h2>
    <ul>
"""
        for innovation in gap_data.get('key_innovations', []):
            html += f"        <li>{innovation}</li>\n"
        
        html += f"""
    </ul>
    
    <h2>Timeline Assessment</h2>
    <div class="subsection">
        <p><strong>Total Timeline:</strong> {gap_data.get('timeline_assessment', {}).get('total_timeline_months', 0)} months</p>
    </div>
    
    <h2>Next Steps</h2>
    <ol>
"""
        for step in gap_data.get('next_steps_for_researcher', []):
            html += f"        <li>{step}</li>\n"
        
        html += f"""
    </ol>
    
    <div class="footer">
        Generated for advisor consultation. Original analysis date: {datetime.now().isoformat()}
    </div>
</body>
</html>
"""
        return html
    
    def _format_summary_text(self, topic: str, gaps: List[Dict[str, Any]]) -> str:
        """Format debate run summary as text."""
        text = f"""
{'='*70}
RESEARCH DEBATE SUMMARY
{'='*70}

Topic: {topic}
Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Gaps Identified: {len(gaps)}

{'─'*70}
TOP 3 GAPS
{'─'*70}
"""
        for i, gap in enumerate(gaps[:3], 1):
            score = gap.get('iclr_readiness_score', 0)
            text += f"\n{i}. {gap.get('gap_title', 'Unknown')}\n"
            text += f"   Readiness: {score}/100\n"
            text += f"   Recommendation: {gap.get('recommendation', 'N/A')}\n"
        
        text += f"""

{'─'*70}
ALL GAPS ({len(gaps)} total)
{'─'*70}
"""
        for i, gap in enumerate(gaps, 1):
            text += f"{i}. {gap.get('gap_title', 'Unknown')} ({gap.get('iclr_readiness_score', 0)}/100)\n"
        
        return text
    
    def _format_summary_html(self, topic: str, gaps: List[Dict[str, Any]]) -> str:
        """Format debate run summary as HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Debate Summary - {topic}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        .gap-row {{ background: #ecf0f1; padding: 10px; margin: 5px 0; border-radius: 5px; }}
        .score {{ float: right; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Research Debate Summary: {topic}</h1>
    <p>Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Total Gaps: {len(gaps)}</p>
    
    <h2>Top 3 Gaps</h2>
"""
        for i, gap in enumerate(gaps[:3], 1):
            html += f"""    <div class="gap-row">
        <strong>{i}. {gap.get('gap_title', 'Unknown')}</strong>
        <span class="score">{gap.get('iclr_readiness_score', 0)}/100</span>
        <p>{gap.get('recommendation', 'N/A')}</p>
    </div>\n"""
        
        html += f"""
    <h2>All Gaps ({len(gaps)} total)</h2>
"""
        for i, gap in enumerate(gaps, 1):
            html += f"""    <div class="gap-row">
        {i}. {gap.get('gap_title', 'Unknown')} - {gap.get('iclr_readiness_score', 0)}/100
    </div>\n"""
        
        html += """
</body>
</html>
"""
        return html
    
    def _sanitize_filename(self, text: str, max_len: int = 50) -> str:
        """Sanitize text for use as filename."""
        import re
        # Replace invalid characters with underscore
        text = re.sub(r'[<>:"/\\|?*]', '_', text)
        # Remove leading/trailing spaces and dots
        text = text.strip('. ')
        # Limit length
        return text[:max_len]
    
    def _create_index(self, gaps: List[Dict[str, Any]], format: str):
        """Create an index file listing all exported gaps."""
        if not config.ENABLE_PDF_EXPORT:
            return
        
        index_file = os.path.join(self.export_dir, f"INDEX_{datetime.now().strftime('%Y%m%d')}.txt")
        
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(f"EXPORTED GAPS INDEX\n")
                f.write(f"Date: {datetime.now().isoformat()}\n")
                f.write(f"Total Gaps: {len(gaps)}\n\n")
                
                for gap in sorted(gaps, key=lambda x: x.get('iclr_readiness_score', 0), reverse=True):
                    f.write(f"{gap.get('gap_title', 'Unknown')} - {gap.get('iclr_readiness_score', 0)}/100\n")
        except:
            pass


def export_for_advisor(gap_data: Dict[str, Any], format: str = "txt") -> str:
    """Convenience function to export a single gap."""
    exporter = AdvisorExporter()
    return exporter.export_gap_analysis(gap_data, format)


def export_debate_summary(topic: str, gaps: List[Dict[str, Any]], format: str = "txt") -> str:
    """Convenience function to export entire debate run."""
    exporter = AdvisorExporter()
    return exporter.export_run_summary(topic, gaps, format)
