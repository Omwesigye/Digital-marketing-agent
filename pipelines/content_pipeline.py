import json
from agentscope.message import Msg
from agents.outputs.content_agent import build_content_agent
from agents.outputs.flier_agent import build_flier_agent
from agents.outputs.video_agent import build_video_agent
from agents.outputs.social_media_agent import build_social_media_agent
from services.supabase_service import SupabaseService
from tools.social_tools import SocialPoster
from schemas.data_models import ContentPiece
from utils.logger import get_logger

logger = get_logger("content_pipeline")

def extract_json(raw_content: str):
    raw = raw_content.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if len(lines) > 2:
            raw = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
    try:
        return json.loads(raw)
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None

def generate_draft_content(insights: list, model_config: str = "gemini_config") -> list:
    """
    Step 1: Content Generation.
    Queries specialized agents (content, flier, video) to draft matching social posts
    and inserts them into the DB with a status of 'draft'.
    """
    logger.info("Starting draft content generation...")
    db = SupabaseService()
    
    content_agent = build_content_agent(model_config)
    flier_agent = build_flier_agent(model_config)
    video_agent = build_video_agent(model_config)

    draft_ids = []

    for insight in insights:
        try:
            insight_title = insight.get("title", "")
            insight_desc = insight.get("description", "")
            insight_id = insight.get("id")

            # 1. Plain Text Post (X)
            prompt_text = (
                f"As a brand promotion manager, create a plain text social post for X (Twitter) based on this insight:\n"
                f"Insight Title: {insight_title}\nInsight Description: {insight_desc}\n"
                f"Format strictly as JSON: {{'platform': 'x', 'format_type': 'text', 'title': 'Title', 'body': 'Post body', 'hashtags': [], 'media_suggestions': []}}"
            )
            res_text = content_agent(Msg(name="system", content=prompt_text, role="system"))
            data_text = extract_json(res_text.content)

            # 2. Promotional Flier (Instagram)
            prompt_flier = (
                f"Create a promotional flier concept for Instagram based on this insight:\n"
                f"Insight Title: {insight_title}\nInsight Description: {insight_desc}\n"
            )
            res_flier = flier_agent(Msg(name="system", content=prompt_flier, role="system"))
            data_flier = extract_json(res_flier.content)

            # 3. Video Script (TikTok)
            prompt_video = (
                f"Create a short-form video concept and script for TikTok based on this insight:\n"
                f"Insight Title: {insight_title}\nInsight Description: {insight_desc}\n"
            )
            res_video = video_agent(Msg(name="system", content=prompt_video, role="system"))
            data_video = extract_json(res_video.content)

            # Combine drafts
            data_list = [d for d in (data_text, data_flier, data_video) if d]

            for data in data_list:
                platform = data.get("platform", "unknown").lower()
                fmt = data.get("format_type", "post")
                draft_post = ContentPiece(
                    content_type="social_post",
                    platform=platform,
                    title=f"[{fmt.upper()}] {data.get('title') or insight_title}",
                    body=data.get("body") or "",
                    hashtags=data.get("hashtags") or [],
                    media_suggestions=data.get("media_suggestions") or [],
                    status="draft",
                    insight_id=insight_id
                )
                
                draft_id = db.insert_content(draft_post)
                draft_ids.append(draft_id)
                logger.info(f"Created {platform} draft ({fmt}) for insight \"{insight_title}\" with ID: {draft_id}")

        except Exception as e:
            logger.error(f"Failed to generate draft content for insight: {e}")

    logger.info(f"Draft content generation complete. Generated {len(draft_ids)} drafts awaiting human review.")
    return draft_ids

def publish_approved_content(model_config: str = "gemini_config") -> int:
    """
    Step 2: Publishing.
    Queries the database for 'approved' content drafts, publishes them using the social tools
    and social media agent, and updates their status to 'published'.
    """
    logger.info("Checking for approved content drafts to publish...")
    db = SupabaseService()
    
    if not db.is_available():
        logger.warning("Database unavailable. Cannot publish approved drafts.")
        return 0

    try:
        # Fetch approved drafts
        res = db.client.table("content_library").select("*").eq("status", "approved").execute()
        approved_items = res.data
    except Exception as e:
        logger.error(f"Failed to fetch approved drafts: {e}")
        return 0

    if not approved_items:
        logger.info("No approved drafts found.")
        return 0

    logger.info(f"Found {len(approved_items)} approved content pieces to publish.")
    social_agent = build_social_media_agent(model_config)
    poster = SocialPoster()
    published_count = 0

    for item in approved_items:
        content_id = item.get("id")
        platform = item.get("platform")
        body = item.get("body")

        logger.info(f"Publishing item {content_id} on {platform}...")
        try:
            # 1. Post to platform
            post_result = {}
            if platform == "twitter":
                post_result = poster.post_to_twitter(body)
            elif platform == "instagram":
                post_result = poster.post_to_instagram(body)
            elif platform == "tiktok":
                post_result = poster.post_to_tiktok(body)
            
            # 2. Inform agent and get status
            agent_prompt = f"Confirm publishing status for this result: {json.dumps(post_result)}"
            response = social_agent(Msg(name="system", content=agent_prompt, role="system"))

            # Update DB status to published
            if post_result.get("status") == "success":
                db.mark_content_published(content_id)
                published_count += 1
                logger.info(f"Successfully published content {content_id} to {platform}.")
            else:
                logger.error(f"Failed to publish content {content_id} to {platform}: {post_result.get('error_message')}")

        except Exception as e:
            logger.error(f"Failed publishing workflow for content {content_id}: {e}")

    return published_count
