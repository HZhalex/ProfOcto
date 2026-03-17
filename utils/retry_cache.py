"""
Smart caching for Gemini API calls to reduce costs and improve speed.
Uses LRU cache with disk persistence.
"""

import json
import hashlib
import os
from functools import wraps
from typing import Callable, Any, Dict
from datetime import datetime, timedelta
import config


class APICache:
    """LRU cache for Gemini API results with disk persistence."""
    
    def __init__(self, cache_dir: str = "phd_analysis/.cache", max_size: int = 500):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.memory_cache: Dict[str, Any] = {}
        self.access_count: Dict[str, int] = {}
        self.timestamps: Dict[str, str] = {}
        
        os.makedirs(cache_dir, exist_ok=True)
        self._load_cache_index()
    
    def _make_key(self, agent_name: str, input_hash: str) -> str:
        """Create cache key from agent name and input hash."""
        return f"{agent_name}_{input_hash[:12]}"
    
    def _hash_input(self, data: Any) -> str:
        """Hash input data for cache key."""
        try:
            serialized = json.dumps(data, sort_keys=True, default=str)
            return hashlib.md5(serialized.encode()).hexdigest()
        except:
            return hashlib.md5(str(data).encode()).hexdigest()
    
    def _load_cache_index(self):
        """Load cache metadata from disk."""
        index_file = os.path.join(self.cache_dir, "_index.json")
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r') as f:
                    data = json.load(f)
                    self.timestamps = data.get("timestamps", {})
                    self.access_count = data.get("access_count", {})
            except:
                pass
    
    def _save_index(self):
        """Save cache metadata to disk."""
        index_file = os.path.join(self.cache_dir, "_index.json")
        try:
            with open(index_file, 'w') as f:
                json.dump({
                    "timestamps": self.timestamps,
                    "access_count": self.access_count
                }, f)
        except:
            pass
    
    def get(self, agent_name: str, input_data: Any) -> Any:
        """Retrieve cached result if exists."""
        if not config.__dict__.get("CACHE_PHASE5_RESULTS", True):
            return None
        
        key = self._make_key(agent_name, self._hash_input(input_data))
        
        # Check memory cache first
        if key in self.memory_cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.memory_cache[key]
        
        # Check disk cache
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    result = json.load(f)
                    self.memory_cache[key] = result
                    self.access_count[key] = self.access_count.get(key, 0) + 1
                    return result
            except:
                pass
        
        return None
    
    def set(self, agent_name: str, input_data: Any, result: Any):
        """Cache result to memory and disk."""
        if not config.__dict__.get("CACHE_PHASE5_RESULTS", True):
            return
        
        key = self._make_key(agent_name, self._hash_input(input_data))
        
        # Store in memory cache
        self.memory_cache[key] = result
        self.access_count[key] = 1
        self.timestamps[key] = datetime.now().isoformat()
        
        # Store on disk
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(result, f, default=str)
        except:
            pass
        
        # Evict LRU item if cache too large
        if len(self.memory_cache) > self.max_size:
            self._evict_lru()
        
        self._save_index()
    
    def _evict_lru(self):
        """Remove least recently used item."""
        if not self.memory_cache:
            return
        
        lru_key = min(self.access_count.keys(), 
                      key=lambda k: self.access_count.get(k, 0))
        
        del self.memory_cache[lru_key]
        del self.access_count[lru_key]
        if lru_key in self.timestamps:
            del self.timestamps[lru_key]
        
        # Also delete from disk
        cache_file = os.path.join(self.cache_dir, f"{lru_key}.json")
        try:
            os.remove(cache_file)
        except:
            pass


# Global cache instance
_api_cache = APICache()


def cached_api_call(agent_name: str):
    """Decorator to cache Gemini API calls."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(input_data: Any, *args, **kwargs) -> Any:
            # Try to get from cache
            cached_result = _api_cache.get(agent_name, input_data)
            if cached_result is not None:
                return cached_result
            
            # Call function
            result = func(input_data, *args, **kwargs)
            
            # Store in cache
            if result:  # Only cache non-empty results
                _api_cache.set(agent_name, input_data, result)
            
            return result
        
        return wrapper
    return decorator


def clear_cache():
    """Clear all cached results."""
    global _api_cache
    _api_cache.memory_cache.clear()
    _api_cache.access_count.clear()
    _api_cache.timestamps.clear()
    
    # Delete cache files
    for f in os.listdir(_api_cache.cache_dir):
        if f.endswith(".json"):
            try:
                os.remove(os.path.join(_api_cache.cache_dir, f))
            except:
                pass


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    return {
        "cached_items": len(_api_cache.memory_cache),
        "total_accesses": sum(_api_cache.access_count.values()),
        "cache_dir": _api_cache.cache_dir
    }
