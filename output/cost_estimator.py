"""
Cost Estimator for API Usage
Estimate API costs and execution timeline before running Phase 5 pipeline.
"""

import config
from typing import Dict, Any
from utils.logger import get_logger


class CostEstimator:
    """Estimate costs and timeline for Phase 5 pipeline."""
    
    # Cost estimates per API call (based on GPT-4 Turbo pricing)
    COST_PER_FORMALIZE_CALL = 0.08  # USD
    COST_PER_NOVELTY_CALL = 0.06    # USD
    COST_PER_SKETCH_CALL = 0.07     # USD
    COST_PER_READINESS_CALL = 0.08  # USD
    
    # Time estimates per operation (seconds)
    TIME_PER_FORMALIZE = 8
    TIME_PER_NOVELTY = 6
    TIME_PER_SKETCH = 10
    TIME_PER_READINESS = 8
    TIME_PER_GAP = (TIME_PER_FORMALIZE + TIME_PER_NOVELTY + TIME_PER_SKETCH + TIME_PER_READINESS)  # 32 seconds
    
    def __init__(self):
        self.logger = get_logger()
    
    def estimate_for_gaps(self, num_gaps: int) -> Dict[str, Any]:
        """
        Estimate cost and time for processing N gaps.
        
        Args:
            num_gaps: Number of gaps to process in Phase 5
            
        Returns:
            {
                'estimated_cost_usd': float,
                'estimated_time_seconds': int,
                'estimated_time_readable': str,
                'cost_breakdown': {...},
                'timeline_breakdown': {...}
            }
        """
        
        # Cost calculation
        cost_formalize = num_gaps * self.COST_PER_FORMALIZE_CALL
        cost_novelty = num_gaps * self.COST_PER_NOVELTY_CALL
        cost_sketch = num_gaps * self.COST_PER_SKETCH_CALL
        cost_readiness = num_gaps * self.COST_PER_READINESS_CALL
        
        total_cost = cost_formalize + cost_novelty + cost_sketch + cost_readiness
        
        # Time calculation
        time_formalize = num_gaps * self.TIME_PER_FORMALIZE
        time_novelty = num_gaps * self.TIME_PER_NOVELTY
        time_sketch = num_gaps * self.TIME_PER_SKETCH
        time_readiness = num_gaps * self.TIME_PER_READINESS
        
        total_time = time_formalize + time_novelty + time_sketch + time_readiness
        
        # Account for caching efficiency
        cache_efficiency = 0.6 if config.USE_RETRY_CACHE else 1.0
        estimated_cost_with_cache = total_cost * cache_efficiency
        estimated_time_with_cache = total_time * cache_efficiency
        
        return {
            'num_gaps': num_gaps,
            'estimated_cost_usd': round(estimated_cost_with_cache, 3),
            'estimated_cost_usd_uncached': round(total_cost, 3),
            'cache_enabled': config.USE_RETRY_CACHE,
            'cache_efficiency': cache_efficiency,
            'estimated_time_seconds': int(estimated_time_with_cache),
            'estimated_time_readable': self._format_time(estimated_time_with_cache),
            'cost_breakdown': {
                'formalize': round(cost_formalize * cache_efficiency, 3),
                'novelty': round(cost_novelty * cache_efficiency, 3),
                'sketch': round(cost_sketch * cache_efficiency, 3),
                'readiness': round(cost_readiness * cache_efficiency, 3)
            },
            'timeline_breakdown': {
                'formalize_seconds': int(time_formalize * cache_efficiency),
                'novelty_seconds': int(time_novelty * cache_efficiency),
                'sketch_seconds': int(time_sketch * cache_efficiency),
                'readiness_seconds': int(time_readiness * cache_efficiency)
            }
        }
    
    def estimate_for_batch(self, num_topics: int) -> Dict[str, Any]:
        """Estimate cost for batch processing multiple topics."""
        # Average gaps per topic
        gaps_per_topic = 5
        total_gaps = num_topics * gaps_per_topic
        
        estimate = self.estimate_for_gaps(total_gaps)
        estimate['num_topics'] = num_topics
        estimate['gaps_per_topic'] = gaps_per_topic
        
        return estimate
    
    def estimate_with_interactive_refinement(self, num_gaps: int, num_refinement_rounds: int = 2) -> Dict[str, Any]:
        """
        Estimate cost including interactive refinement phase.
        Each refinement round re-processes ~30% of gaps.
        """
        base_estimate = self.estimate_for_gaps(num_gaps)
        
        # Additional cost for refinements
        refinement_cost = 0
        refinement_time = 0
        
        for round_num in range(num_refinement_rounds):
            gaps_to_refine = int(num_gaps * 0.3)  # Only 30% need refinement
            round_cost = gaps_to_refine * self.COST_PER_READINESS_CALL
            round_time = gaps_to_refine * self.TIME_PER_READINESS
            
            refinement_cost += round_cost
            refinement_time += round_time
        
        total_cost = base_estimate['estimated_cost_usd'] + refinement_cost
        total_time = base_estimate['estimated_time_seconds'] + refinement_time
        
        return {
            **base_estimate,
            'refinement_rounds': num_refinement_rounds,
            'refinement_cost': round(refinement_cost, 3),
            'refinement_time_seconds': int(refinement_time),
            'total_cost_with_refinement': round(total_cost, 3),
            'total_time_with_refinement': int(total_time),
            'total_time_with_refinement_readable': self._format_time(total_time)
        }
    
    def format_cost_summary(self, estimate: Dict[str, Any]) -> str:
        """Format estimate as readable summary."""
        summary = f"""
Cost & Timeline Estimate
{'─'*50}

Gaps to Process: {estimate['num_gaps']}
Estimated API Cost: ${estimate['estimated_cost_usd']}
Estimated Runtime: {estimate['estimated_time_readable']}

Cost Breakdown:
  • Gap Formalization: ${estimate['cost_breakdown']['formalize']}
  • Novelty Analysis: ${estimate['cost_breakdown']['novelty']}
  • Solution Sketching: ${estimate['cost_breakdown']['sketch']}
  • Readiness Scoring: ${estimate['cost_breakdown']['readiness']}

Cache Status: {"Enabled (60% cost reduction)" if estimate['cache_enabled'] else "Disabled"}
"""
        
        if 'refinement_cost' in estimate and estimate['refinement_cost'] > 0:
            summary += f"""
Refinement Estimate (interactive phase):
  • Rounds: {estimate['refinement_rounds']}
  • Cost: ${estimate['refinement_cost']}
  • Time: {self._format_time(estimate['refinement_time_seconds'])}
  
Total with Refinement:
  • Cost: ${estimate['total_cost_with_refinement']}
  • Time: {estimate['total_time_with_refinement_readable']}
"""
        
        return summary
    
    def should_confirm_cost(self, estimate: Dict[str, Any]) -> bool:
        """Determine if cost needs user confirmation."""
        cost = estimate['estimated_cost_usd']
        
        # Ask for confirmation if:
        # 1. Cost > $0.50
        # 2. Time > 5 minutes
        # 3. Cost > %50 of budget (if set)
        
        if cost > config.COST_CONFIRMATION_THRESHOLD:
            return True
        
        time_seconds = estimate['estimated_time_seconds']
        if time_seconds > 300:  # 5 minutes
            return True
        
        if hasattr(config, 'MONTHLY_BUDGET_USD') and config.MONTHLY_BUDGET_USD:
            if cost > config.MONTHLY_BUDGET_USD * 0.5:
                return True
        
        return False
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds to readable time."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"


def estimate_cost_for_gaps(num_gaps: int) -> Dict[str, Any]:
    """Convenience function to get cost estimate."""
    estimator = CostEstimator()
    return estimator.estimate_for_gaps(num_gaps)


def format_cost_estimate(num_gaps: int) -> str:
    """Convenience function to get formatted cost estimate."""
    estimator = CostEstimator()
    estimate = estimator.estimate_for_gaps(num_gaps)
    return estimator.format_cost_summary(estimate)
