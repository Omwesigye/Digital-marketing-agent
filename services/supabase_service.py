import os
from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
from schemas.data_models import (
    RawSignal, SentimentResult, CompetitorInsight, 
    Insight, ContentPiece, Campaign, EmailContact, EmailSend
)
from utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

logger = get_logger("supabase_service")

# Initialize client safely
supabase = None
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    url_to_use = SUPABASE_URL
    if SUPABASE_URL.startswith("postgresql://"):
        try:
            # Extract host db.xxxx.supabase.co
            host = SUPABASE_URL.split("@")[-1].split(":")[0]
            if host.startswith("db."):
                project_ref = host.split(".")[1]
                url_to_use = f"https://{project_ref}.supabase.co"
                logger.info(f"Converted Supabase PostgreSQL connection string to REST API URL: {url_to_use}")
        except Exception as e:
            logger.error(f"Failed to parse PostgreSQL URL: {e}")

    try:
        supabase = create_client(url_to_use, SUPABASE_SERVICE_ROLE_KEY)
        logger.info("Supabase client successfully initialized.")
    except Exception as e:
        logger.error(f"Error initializing Supabase client: {e}")
else:
    logger.warning("Supabase environment variables missing. Database operations will be mocked/skipped.")

class SupabaseService:
    def __init__(self):
        self.client = supabase

    def is_available(self) -> bool:
        return self.client is not None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def insert_signals(self, signals: list) -> list:
        if not self.is_available():
            logger.warning("Supabase not available. Mocking signal insertion.")
            return [f"mock-id-{i}" for i in range(len(signals))]
        
        inserted_ids = []
        for sig in signals:
            try:
                # Convert model to dict, serialize datetimes via mode='json'
                data = sig.model_dump(mode='json', exclude_none=True) if hasattr(sig, "model_dump") else sig
                result = self.client.table("raw_signals").insert(data).execute()
                if result.data:
                    inserted_ids.append(result.data[0]["id"])
            except Exception as e:
                logger.error(f"Failed to insert raw signal: {e}")
        return inserted_ids

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def insert_sentiments(self, results: list) -> None:
        if not self.is_available():
            return
        for res in results:
            try:
                data = res.model_dump(mode='json', exclude_none=True) if hasattr(res, "model_dump") else res
                self.client.table("sentiment_results").insert(data).execute()
            except Exception as e:
                logger.error(f"Failed to insert sentiment result: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def insert_competitor_insight(self, insight) -> None:
        if not self.is_available():
            return
        try:
            data = insight.model_dump(mode='json', exclude_none=True) if hasattr(insight, "model_dump") else insight
            self.client.table("competitor_insights").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to insert competitor insight: {e}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def insert_insight(self, insight) -> str:
        if not self.is_available():
            return "mock-insight-id"
        try:
            data = insight.model_dump(mode='json', exclude_none=True) if hasattr(insight, "model_dump") else insight
            result = self.client.table("insights").insert(data).execute()
            if result.data:
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to insert insight: {e}")
        return ""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def insert_content(self, content) -> str:
        if not self.is_available():
            return "mock-content-id"
        try:
            data = content.model_dump(mode='json', exclude_none=True) if hasattr(content, "model_dump") else content
            result = self.client.table("content_library").insert(data).execute()
            if result.data:
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to insert content draft: {e}")
        return ""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def insert_campaign(self, campaign) -> str:
        if not self.is_available():
            return "mock-campaign-id"
        try:
            data = campaign.model_dump(mode='json', exclude_none=True) if hasattr(campaign, "model_dump") else campaign
            result = self.client.table("campaigns").insert(data).execute()
            if result.data:
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to insert campaign: {e}")
        return ""

    def get_recent_signals(self, limit: int = 50) -> list:
        if not self.is_available():
            return []
        try:
            result = self.client.table("raw_signals").select("*").order("scraped_at", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to fetch recent signals: {e}")
            return []

    def get_pending_content(self) -> list:
        """Fetch content drafts waiting for human approval."""
        if not self.is_available():
            return []
        try:
            result = self.client.table("content_library").select("*").eq("status", "draft").execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to fetch pending content: {e}")
            return []

    def approve_content(self, content_id: str) -> bool:
        """Approve a draft content so it can be published."""
        if not self.is_available():
            return True
        try:
            result = self.client.table("content_library").update({"status": "approved"}).eq("id", content_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Failed to approve content: {e}")
            return False

    def mark_content_published(self, content_id: str) -> bool:
        if not self.is_available():
            return True
        import datetime
        try:
            result = self.client.table("content_library").update({
                "status": "published", 
                "published_at": datetime.datetime.now().isoformat()
            }).eq("id", content_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Failed to mark content published: {e}")
            return False

    def get_email_contacts(self) -> list:
        if not self.is_available():
            return [
                {"id": "mock-contact-1", "email": "regular@example.com", "name": "Regular Joe", "segment": "regular"},
                {"id": "mock-contact-2", "email": "churning@example.com", "name": "Churning Jane", "segment": "churning"},
                {"id": "mock-contact-3", "email": "vip@example.com", "name": "VIP Sam", "segment": "vip"},
            ]
        try:
            result = self.client.table("email_contacts").select("*").eq("unsubscribed", False).execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to fetch email contacts: {e}")
            return []

    def record_email_send(self, email_send) -> None:
        if not self.is_available():
            return
        try:
            data = email_send.model_dump(mode='json', exclude_none=True) if hasattr(email_send, "model_dump") else email_send
            self.client.table("email_sends").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to record email send: {e}")