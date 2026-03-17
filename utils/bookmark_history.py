"""
Gap Bookmarking & Run History Management
Track favorite gaps and previous debate runs for comparison.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import config
from utils.logger import get_logger


class GapBookmarkManager:
    """Manage bookmarked (favorite) gaps."""
    
    def __init__(self, bookmark_file: str = None):
        self.bookmark_file = bookmark_file or config.BOOKMARK_FILE
        os.makedirs(os.path.dirname(self.bookmark_file), exist_ok=True)
        self.bookmarks: List[Dict[str, Any]] = []
        self._load_bookmarks()
    
    def _load_bookmarks(self):
        """Load bookmarks from file."""
        if os.path.exists(self.bookmark_file):
            try:
                with open(self.bookmark_file, 'r', encoding='utf-8') as f:
                    self.bookmarks = json.load(f)
            except:
                self.bookmarks = []
    
    def _save_bookmarks(self):
        """Save bookmarks to file."""
        try:
            with open(self.bookmark_file, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            get_logger().log_error("bookmarks", e, context="Failed to save bookmarks")
    
    def bookmark(self, gap_title: str, readiness_data: Dict[str, Any], notes: str = ""):
        """Add a gap to bookmarks."""
        # Check if already bookmarked
        if any(b.get("gap_title") == gap_title for b in self.bookmarks):
            return False
        
        entry = {
            "gap_title": gap_title,
            "bookmarked_at": datetime.now().isoformat(),
            "readiness_score": readiness_data.get("iclr_readiness_score", 0),
            "recommendation": readiness_data.get("recommendation", ""),
            "timeline_months": readiness_data.get("timeline_assessment", {}).get("total_timeline_months", 0),
            "notes": notes,
            "full_data": readiness_data  # Store full analysis
        }
        
        self.bookmarks.append(entry)
        self._save_bookmarks()
        get_logger().gap_logger.info(f"Bookmarked gap: {gap_title}")
        return True
    
    def remove_bookmark(self, gap_title: str) -> bool:
        """Remove a gap from bookmarks."""
        initial_count = len(self.bookmarks)
        self.bookmarks = [b for b in self.bookmarks if b.get("gap_title") != gap_title]
        
        if len(self.bookmarks) < initial_count:
            self._save_bookmarks()
            return True
        return False
    
    def get_bookmarks(self) -> List[Dict[str, Any]]:
        """Get all bookmarked gaps."""
        return self.bookmarks
    
    def get_bookmark(self, gap_title: str) -> Optional[Dict[str, Any]]:
        """Get a specific bookmark."""
        for b in self.bookmarks:
            if b.get("gap_title") == gap_title:
                return b
        return None
    
    def update_notes(self, gap_title: str, notes: str) -> bool:
        """Update notes for a bookmarked gap."""
        for b in self.bookmarks:
            if b.get("gap_title") == gap_title:
                b["notes"] = notes
                b["updated_at"] = datetime.now().isoformat()
                self._save_bookmarks()
                return True
        return False


class RunHistoryManager:
    """Track and compare multiple debate runs."""
    
    def __init__(self, history_file: str = None):
        self.history_file = history_file or config.HISTORY_FILE
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        self.history: List[Dict[str, Any]] = []
        self._load_history()
    
    def _load_history(self):
        """Load run history from file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def _save_history(self):
        """Save run history to file."""
        try:
            # Keep only last MAX_HISTORY_ENTRIES entries
            self.history = self.history[-config.MAX_HISTORY_ENTRIES:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            get_logger().log_error("history", e, context="Failed to save history")
    
    def record_run(self, topic: str, field: str, readiness_scores: List[Dict[str, Any]]):
        """Record a debate run."""
        run_entry = {
            "run_id": f"{topic[:20]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic": topic,
            "field": field,
            "run_at": datetime.now().isoformat(),
            "num_gaps": len(readiness_scores),
            "top_gap": readiness_scores[0].get("gap_title") if readiness_scores else None,
            "top_gap_score": readiness_scores[0].get("iclr_readiness_score", 0) if readiness_scores else 0,
            "avg_score": sum(r.get("iclr_readiness_score", 0) for r in readiness_scores) / len(readiness_scores) if readiness_scores else 0,
            "gap_list": [(r.get("gap_title"), r.get("iclr_readiness_score", 0)) for r in readiness_scores]
        }
        
        self.history.append(run_entry)
        self._save_history()
        get_logger().gap_logger.info(f"Recorded run: {topic}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get all runs."""
        return self.history
    
    def get_recent_runs(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get last N runs."""
        return self.history[-n:]
    
    def find_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Find a specific run by ID."""
        for run in self.history:
            if run.get("run_id") == run_id:
                return run
        return None
    
    def compare_runs(self, run_id1: str, run_id2: str) -> Dict[str, Any]:
        """Compare two runs."""
        run1 = self.find_run(run_id1)
        run2 = self.find_run(run_id2)
        
        if not run1 or not run2:
            return {}
        
        # Find common gaps
        gaps1 = set(g[0] for g in run1.get("gap_list", []))
        gaps2 = set(g[0] for g in run2.get("gap_list", []))
        
        common = gaps1 & gaps2
        only_in_1 = gaps1 - gaps2
        only_in_2 = gaps2 - gaps1
        
        return {
            "run1_topic": run1.get("topic"),
            "run1_time": run1.get("run_at"),
            "run2_topic": run2.get("topic"),
            "run2_time": run2.get("run_at"),
            "common_gaps": list(common),
            "only_in_first": list(only_in_1),
            "only_in_second": list(only_in_2),
            "avg_score_1": run1.get("avg_score"),
            "avg_score_2": run2.get("avg_score"),
            "score_improved": run2.get("avg_score", 0) > run1.get("avg_score", 0)
        }


def get_bookmark_manager() -> GapBookmarkManager:
    """Get global bookmark manager."""
    return GapBookmarkManager()


def get_history_manager() -> RunHistoryManager:
    """Get global history manager."""
    return RunHistoryManager()
