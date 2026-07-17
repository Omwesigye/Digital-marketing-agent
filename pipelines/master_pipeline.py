import time
import schedule
from pipelines.listening_pipeline import run_listening_pipeline
from pipelines.analysis_pipeline import run_analysis_pipeline
from pipelines.content_pipeline import generate_draft_content, publish_approved_content
from pipelines.campaign_pipeline import run_campaign_pipeline
from utils.logger import get_logger

logger = get_logger("master_pipeline")

def run_full_listening_and_insights_pipeline(model_config: str = "gemini_config") -> list:
    """
    Runs the listening, cleaning, storage, sentiment analysis, competitor tracking,
    and content drafting end-to-end. Keeps draft content in draft status for human approval.
    """
    logger.info("========================================")
    logger.info("STARTING MASTER RESTAURANT AGENT RUN")
    logger.info("========================================")

    import agentscope
    import os
    config_path = os.path.join("config", "model_config.json")
    try:
        agentscope.init(model_configs=config_path)
    except Exception:
        pass

    # 1. Listen & Ingest
    logger.info("--- Phase 2: Ingesting Signals ---")
    signal_ids = run_listening_pipeline()
    if not signal_ids:
        logger.warning("No new signals collected. Master run finished early.")
        return []

    # 2. Analyze & Synthesize
    logger.info("--- Phase 3: Analyzing Sentiment & Competitors ---")
    insights = run_analysis_pipeline(signal_ids=signal_ids, model_config=model_config)
    if not insights:
        logger.warning("No insights generated. Master run finished.")
        return []

    # 3. Draft Campaigns & Content
    logger.info("--- Phase 4: Drafting Content (Human-in-the-loop) ---")
    draft_ids = generate_draft_content(insights=insights, model_config=model_config)
    
    logger.info("========================================")
    logger.info(f"MASTER RUN COMPLETE. Generated {len(draft_ids)} drafts awaiting dashboard approval.")
    logger.info("========================================")
    return draft_ids

def run_retention_campaign(campaign_name: str, goal: str, model_config: str = "gemini_config") -> dict:
    """Runs Phase 5 email retention campaign directly."""
    logger.info("--- Phase 5: Executing retention email campaign ---")
    result = run_campaign_pipeline(campaign_name=campaign_name, goal=goal, model_config=model_config)
    return result

def run_publishing_cycle(model_config: str = "gemini_config") -> int:
    """Checks DB for approved posts and publishes them to mock/real APIs."""
    logger.info("--- Phase 4: Publishing approved content cycle ---")
    published = publish_approved_content(model_config=model_config)
    return published

def start_realtime_listener(interval_seconds: int = 300, model_config: str = "gemini_config"):
    """
    Runs the pipeline continuously at a regular polling interval (real-time mode).
    """
    logger.info(f"Starting real-time continuous restaurant listener (polling every {interval_seconds}s)...")
    
    # Run once immediately
    try:
        run_full_listening_and_insights_pipeline(model_config=model_config)
    except Exception as e:
        logger.error(f"Error during initial real-time run: {e}")

    schedule.every(interval_seconds).seconds.do(
        run_full_listening_and_insights_pipeline, model_config=model_config
    )

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logger.error(f"Error in scheduled real-time loop: {e}")
        time.sleep(1)
