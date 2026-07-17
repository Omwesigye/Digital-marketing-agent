from services.supabase_service import SupabaseService
from utils.logger import get_logger

logger = get_logger("shared_memory")

class SharedMemory:
    """
    Interface for cross-agent memory, backing up conversational/state variables
    into Supabase relational tables. Allows agents to share learnings across sessions.
    """
    def __init__(self):
        self.db = SupabaseService()

    def store_brand_learning(self, competitor_name: str, key: str, val: str):
        """Saves a learned competitor tactic or brand behavior."""
        logger.info(f"[SharedMemory] Storing learning for {competitor_name}: {key}={val}")
        if not self.db.is_available():
            return
        
        try:
            # Upsert into competitor insights or raw metadata for shared access
            data = {
                "competitor_name": competitor_name,
                "metric_type": f"learning_{key}",
                "metric_value": 1.0,
                "details": {"note": val}
            }
            self.db.client.table("competitor_insights").insert(data).execute()
        except Exception as e:
            logger.error(f"[SharedMemory] Failed to store brand learning: {e}")

    def get_recent_learnings(self, limit: int = 10) -> list:
        """Retrieves recently logged brand and competitor learnings."""
        if not self.db.is_available():
            return []
        
        try:
            res = self.db.client.table("competitor_insights")\
                .select("*")\
                .like("metric_type", "learning_%")\
                .order("tracked_at", desc=True)\
                .limit(limit)\
                .execute()
            return res.data
        except Exception as e:
            logger.error(f"[SharedMemory] Failed to retrieve brand learnings: {e}")
            return []
