import json
from agentscope.message import Msg

from agents.outputs.campaign_agent import build_campaign_agent
from agents.outputs.content_agent import build_content_agent
from agents.outputs.email_agent import build_email_agent
from services.supabase_service import SupabaseService
from tools.email_tools import EmailManager
from schemas.data_models import Campaign, EmailSend
from utils.logger import get_logger

logger = get_logger("campaign_pipeline")

def run_campaign_pipeline(campaign_name: str, goal: str, model_config: str = "gemini_config") -> dict:
    """
    Orchestrates Phase 5:
    1. Sets up the campaign in the database.
    2. Runs campaign coordination using AgentScope MsgHub.
    3. Segments customers, creates tailored emails, and sends them via Resend.
    4. Logs campaign execution results.
    """
    logger.info(f"Starting campaign pipeline for: \"{campaign_name}\"...")
    db = SupabaseService()
    email_mgr = EmailManager()

    # 1. Register campaign in DB
    campaign_model = Campaign(
        name=campaign_name,
        goal=goal,
        channels=["email"],
        status="active"
    )
    campaign_id = db.insert_campaign(campaign_model)
    logger.info(f"Campaign registered with ID: {campaign_id}")

    # 2. Get contacts for segmentation
    contacts = db.get_email_contacts()
    if not contacts:
        logger.warning("No active email contacts found. Exiting campaign pipeline.")
        return {"status": "skipped", "reason": "no contacts"}

    # 3. Instantiate agents
    campaign_agent = build_campaign_agent(model_config)
    content_agent = build_content_agent(model_config)
    email_agent = build_email_agent(model_config)

    # 4. Run coordinated campaign workflow
    logger.info("Executing campaign orchestration...")
    sends_logged = 0

    for contact in contacts:
        try:
            name = contact.get("name") or "Valued Guest"
            email = contact.get("email")
            segment = contact.get("segment") or "regular"

            # Prompt campaign flow to decide/draft content
            prompt = (
                f"Orchestrate a loyalty outreach for customer {name} (Segment: {segment}) "
                f"for campaign goal: '{goal}'. Draft a personalized subject and email body."
            )
            response = email_agent(Msg(name="system", content=prompt, role="system"))

            # Parse email subject and body
            raw_content = response.content.strip()
            if raw_content.startswith("```"):
                lines = raw_content.splitlines()
                if len(lines) > 2:
                    raw_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])

            try:
                data = json.loads(raw_content)
                subject = data.get("title") or f"Special Restaurant Offer for {name}!"
                body = data.get("body") or response.content
            except Exception:
                subject = f"Special Restaurant Offer for {name}!"
                body = response.content

            # Save as draft instead of auto-sending
            from schemas.data_models import ContentPiece
            draft_email = ContentPiece(
                content_type="email_draft",
                platform="email",
                title=f"[DRAFT EMAIL] {subject}",
                body=body,
                hashtags=[],
                media_suggestions=[],
                status="draft",
                insight_id=contact.get("id") # Using contact id to track recipient
            )
            
            draft_id = db.insert_content(draft_email)
            sends_logged += 1
            logger.info(f"Successfully saved draft email to {email} with ID: {draft_id}")

        except Exception as e:
                logger.error(f"Error executing campaign for contact {contact.get('email')}: {e}")

    logger.info(f"Campaign pipeline complete. Saved {sends_logged} draft loyalty emails.")
    return {"status": "completed", "campaign_id": campaign_id, "drafts_saved": sends_logged}
