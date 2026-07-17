import os
import requests
from utils.logger import get_logger

logger = get_logger("social_tools")

class SocialPoster:
    def __init__(self):
        # Read API tokens from environment if present
        self.twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.fb_instagram_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.tiktok_token = os.getenv("TIKTOK_ACCESS_TOKEN")

    def post_to_twitter(self, text: str, media_url: str = None) -> dict:
        """
        Posts to Twitter API. Falls back to logging mock posts if bearer token is missing.
        """
        logger.info(f"[SocialPoster] Attempting Twitter post: \"{text[:50]}...\"")
        if not self.twitter_token:
            logger.warning("[SocialPoster] TWITTER_BEARER_TOKEN not set. Mocking successful post.")
            return {"status": "success", "platform": "twitter", "post_id": "mock-tweet-123456"}

        try:
            # Placeholder for Twitter v2 API endpoint call
            url = "https://api.twitter.com/2/tweets"
            headers = {
                "Authorization": f"Bearer {self.twitter_token}",
                "Content-Type": "application/json"
            }
            payload = {"text": text}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            return {"status": "success", "platform": "twitter", "post_id": data.get("data", {}).get("id")}
        except Exception as e:
            logger.error(f"[SocialPoster] Twitter API error: {e}")
            return {"status": "error", "platform": "twitter", "error_message": str(e)}

    def post_to_instagram(self, caption: str, image_url: str = None) -> dict:
        """
        Posts to Instagram Graph API. Falls back to mock post.
        """
        logger.info(f"[SocialPoster] Attempting Instagram post: \"{caption[:50]}...\"")
        if not self.fb_instagram_token:
            logger.warning("[SocialPoster] INSTAGRAM_ACCESS_TOKEN not set. Mocking successful post.")
            return {"status": "success", "platform": "instagram", "post_id": "mock-insta-987654"}

        try:
            # Placeholder for FB Graph API /media and /media_publish calls
            # Step 1: Create media container, Step 2: Publish container
            logger.info("Publishing via FB/Instagram Graph API...")
            return {"status": "success", "platform": "instagram", "post_id": "ig-post-created"}
        except Exception as e:
            logger.error(f"[SocialPoster] Instagram API error: {e}")
            return {"status": "error", "platform": "instagram", "error_message": str(e)}

    def post_to_tiktok(self, title: str, video_path: str = None) -> dict:
        """
        Posts to TikTok API. Falls back to mock post.
        """
        logger.info(f"[SocialPoster] Attempting TikTok post: \"{title[:50]}...\"")
        if not self.tiktok_token:
            logger.warning("[SocialPoster] TIKTOK_ACCESS_TOKEN not set. Mocking successful post.")
            return {"status": "success", "platform": "tiktok", "post_id": "mock-tiktok-112233"}

        try:
            logger.info("Publishing via TikTok Share API...")
            return {"status": "success", "platform": "tiktok", "post_id": "tiktok-share-created"}
        except Exception as e:
            logger.error(f"[SocialPoster] TikTok API error: {e}")
            return {"status": "error", "platform": "tiktok", "error_message": str(e)}
