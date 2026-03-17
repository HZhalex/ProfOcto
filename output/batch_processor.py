"""
Batch Processor for Multiple Debates
Run debates on multiple topics and aggregate findings for robust gap identification.
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import config
from utils.logger import get_logger


class BatchProcessor:
    """Process multiple debate topics in batch mode."""
    
    def __init__(self, batch_file: str = None):
        self.batch_file = batch_file or config.BATCH_FILE
        self.logger = get_logger()
        self.results: List[Dict[str, Any]] = []
        self.gap_frequency: Dict[str, int] = {}
        self.topic_results: Dict[str, Dict[str, Any]] = {}
    
    def load_batch(self) -> List[Dict[str, str]]:
        """Load topics from CSV file."""
        if not os.path.exists(self.batch_file):
            self.logger.gap_logger.warning(f"Batch file not found: {self.batch_file}")
            return []
        
        topics = []
        try:
            with open(self.batch_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('topic'):
                        topics.append({
                            'topic': row['topic'].strip(),
                            'field': row.get('field', 'General AI').strip(),
                            'skip': row.get('skip', 'no').lower() == 'yes'
                        })
        except Exception as e:
            self.logger.log_error("batch_processor", e, context="Failed to load batch file")
            return []
        
        return topics
    
    def process_topics(self, topics: List[Dict[str, str]], 
                      debate_runner) -> Dict[str, Any]:
        """
        Run debates on multiple topics.
        
        Args:
            topics: List of {'topic': str, 'field': str}
            debate_runner: Function that runs a single debate and returns gaps
            
        Returns:
            Aggregated results across all topics
        """
        if not config.ENABLE_BATCH_MODE:
            return {}
        
        self.results = []
        self.gap_frequency = {}
        self.topic_results = {}
        
        total_topics = len([t for t in topics if not t.get('skip')])
        processed = 0
        
        for topic_entry in topics:
            if topic_entry.get('skip'):
                self.logger.gap_logger.info(f"Skipping {topic_entry['topic']} (marked skip)")
                continue
            
            topic = topic_entry['topic']
            field = topic_entry.get('field', 'General AI')
            
            processed += 1
            self.logger.gap_logger.info(f"Processing {processed}/{total_topics}: {topic}")
            
            try:
                # Run debate (using provided runner function)
                gaps = debate_runner(topic, field)
                
                # Record results
                run_result = {
                    'topic': topic,
                    'field': field,
                    'status': 'success',
                    'num_gaps': len(gaps),
                    'gaps': gaps,
                    'processed_at': datetime.now().isoformat()
                }
                
                self.results.append(run_result)
                self.topic_results[topic] = run_result
                
                # Track gap frequency
                for gap in gaps:
                    gap_title = gap.get('gap_title', 'Unknown')
                    self.gap_frequency[gap_title] = self.gap_frequency.get(gap_title, 0) + 1
                
            except Exception as e:
                self.logger.log_error("batch_processor", e, context=f"Failed to process {topic}")
                self.results.append({
                    'topic': topic,
                    'field': field,
                    'status': 'failed',
                    'error': str(e),
                    'processed_at': datetime.now().isoformat()
                })
        
        return self._aggregate_results()
    
    def _aggregate_results(self) -> Dict[str, Any]:
        """Aggregate results across all topics."""
        # Find gaps that appear in multiple topics
        recurring_gaps = {
            gap_title: count 
            for gap_title, count in self.gap_frequency.items() 
            if count > 1
        }
        
        # Sort by frequency
        recurring_gaps = dict(sorted(recurring_gaps.items(), key=lambda x: x[1], reverse=True))
        
        # Calculate statistics
        successful_runs = len([r for r in self.results if r.get('status') == 'success'])
        total_runs = len(self.results)
        total_gaps_found = sum(r.get('num_gaps', 0) for r in self.results)
        
        return {
            'summary': {
                'total_topics': total_runs,
                'successful_runs': successful_runs,
                'failed_runs': total_runs - successful_runs,
                'total_gaps_found': total_gaps_found,
                'recurring_gaps_count': len(recurring_gaps),
                'processed_at': datetime.now().isoformat()
            },
            'recurring_gaps': recurring_gaps,
            'topic_results': self.topic_results,
            'all_results': self.results
        }
    
    def get_recurring_gaps(self, min_frequency: int = 2) -> List[Dict[str, Any]]:
        """Get gaps that appear in multiple topics."""
        recurring = []
        
        for gap_title, frequency in sorted(self.gap_frequency.items(), key=lambda x: x[1], reverse=True):
            if frequency >= min_frequency:
                # Get most trustworthy version of this gap (from highest-readiness analysis)
                best_version = None
                best_score = 0
                
                for result in self.results:
                    for gap in result.get('gaps', []):
                        if gap.get('gap_title') == gap_title:
                            score = gap.get('iclr_readiness_score', 0)
                            if score > best_score:
                                best_score = score
                                best_version = gap
                
                if best_version:
                    best_version['recurrence_count'] = frequency
                    best_version['appears_in_topics'] = [
                        r['topic'] for r in self.results 
                        if any(g.get('gap_title') == gap_title for g in r.get('gaps', []))
                    ]
                    recurring.append(best_version)
        
        return recurring
    
    def export_batch_results(self, output_file: str = None) -> str:
        """Export batch results to JSON."""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(config.BATCH_RESULTS_DIR, f"batch_results_{timestamp}.json")
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self._aggregate_results(), f, indent=2, ensure_ascii=False)
            
            self.logger.gap_logger.info(f"Exported batch results to {output_file}")
            return output_file
        except Exception as e:
            self.logger.log_error("batch_processor", e, context="Failed to export batch results")
            return ""
    
    def create_batch_template(self) -> str:
        """Create a template batch CSV file."""
        template_file = self.batch_file
        os.makedirs(os.path.dirname(template_file), exist_ok=True)
        
        try:
            with open(template_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['topic', 'field', 'skip'])
                writer.writerow(['', 'General AI', 'no'])
            
            self.logger.gap_logger.info(f"Created batch template at {template_file}")
            return template_file
        except Exception as e:
            self.logger.log_error("batch_processor", e, context="Failed to create batch template")
            return ""


def run_batch_process(topics: List[Dict[str, str]], debate_runner) -> Dict[str, Any]:
    """Convenience function to run batch processing."""
    processor = BatchProcessor()
    return processor.process_topics(topics, debate_runner)


def get_recurring_gaps(min_frequency: int = 2) -> List[Dict[str, Any]]:
    """Get gaps appearing in multiple batch runs."""
    processor = BatchProcessor()
    processor.results = json.load(open(config.HISTORY_FILE, 'r')) if os.path.exists(config.HISTORY_FILE) else []
    return processor.get_recurring_gaps(min_frequency)
