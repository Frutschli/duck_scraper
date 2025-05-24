import json
import os
from threading import Lock

class CacheManager:
    _cache_file = "company_cache.json"
    _lock = Lock()
    
    @classmethod
    def load_cache(cls):
        if not os.path.exists(cls._cache_file):
            return {}
        with open(cls._cache_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    
    @classmethod
    def save_cache(cls, cache_data):
        with cls._lock:
            with open(cls._cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def get_company(cls, name):
        cache = cls.load_cache()
        return cache.get(name)
    
    @classmethod
    def update_company(cls, name, data):
        cache = cls.load_cache()
        cache[name] = data
        cls.save_cache(cache)

    @classmethod
    def clear_cache(cls):
        """Clear the entire cache by saving an empty dictionary."""
        cls.save_cache({})

    @classmethod
    def get_all_relevant_data(cls):
        """Extract and return all relevant data fields from the cache."""
        cache = cls.load_cache()
        data = next(iter(cache.values()))

        filtered_data = {
            k: v for k, v in data.items()
            if k not in ("company_name", "urls")
        }
        print(filtered_data)
        return filtered_data
