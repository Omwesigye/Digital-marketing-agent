import os
import json
import hashlib
from functools import wraps
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.logger import get_logger

logger = get_logger("etl_helpers")

def with_retry(max_attempts=3):
    """
    Decorator for robust rate limiting and error handling.
    Uses exponential backoff to handle transient API/network errors gracefully.
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )

def disk_cache(ttl_hours=12):
    """
    Decorator that caches the result of a function to disk as JSON.
    Useful for not repeatedly hitting paid APIs (like Apify) during development
    or within the same crawling window.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Ensure cache directory exists
            cache_dir = os.path.join("data", "cache")
            os.makedirs(cache_dir, exist_ok=True)

            # Create a unique cache key based on function name and arguments
            key_string = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            key_hash = hashlib.md5(key_string.encode('utf-8')).hexdigest()
            cache_file = os.path.join(cache_dir, f"{key_hash}.json")

            # Check if valid cache exists
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    cache_time = datetime.fromisoformat(cached_data['timestamp'])
                    if datetime.now() - cache_time < timedelta(hours=ttl_hours):
                        logger.info(f"Loaded cached data for {func.__name__} (Key: {key_hash})")
                        return cached_data['data']
                    else:
                        logger.info(f"Cache expired for {func.__name__} (Key: {key_hash})")
                except Exception as e:
                    logger.warning(f"Failed to read cache {cache_file}: {e}")

            # Execute the actual function
            result = func(self, *args, **kwargs)

            # Serialize and save to cache
            try:
                # We need to ensure the result is JSON serializable. 
                # Pydantic models need to be dicts. 
                # Our tools will return lists of dicts or pydantic objects.
                # Let's handle Pydantic objects if present.
                serializable_result = []
                if isinstance(result, list):
                    for item in result:
                        if hasattr(item, "dict"):
                            # It's a pydantic model
                            # convert datetime inside to string
                            item_dict = item.dict()
                            for k, v in item_dict.items():
                                if isinstance(v, datetime):
                                    item_dict[k] = v.isoformat()
                            serializable_result.append(item_dict)
                        else:
                            serializable_result.append(item)
                else:
                    serializable_result = result

                cache_payload = {
                    "timestamp": datetime.now().isoformat(),
                    "data": serializable_result
                }
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_payload, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved new cache for {func.__name__} (Key: {key_hash})")
            except Exception as e:
                logger.warning(f"Failed to write cache to {cache_file}: {e}")

            return result
        return wrapper
    return decorator
