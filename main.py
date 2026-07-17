import argparse
import os
import uvicorn
import agentscope
from dotenv import load_dotenv

# Load env variables before loading config
load_dotenv()

from pipelines.master_pipeline import (
    run_full_listening_and_insights_pipeline,
    run_retention_campaign,
    run_publishing_cycle,
    start_realtime_listener
)
from pipelines.listening_pipeline import run_listening_pipeline
from pipelines.analysis_pipeline import run_analysis_pipeline
from config.settings import POLLING_INTERVAL_SECONDS
from utils.logger import get_logger

# FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

logger = get_logger("main")

# Initialize the FastAPI App instance
app = FastAPI(title="Digital Marketing Assistant API")

# Configure CORS middleware for local frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Render deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the modular API endpoints route architecture
app.include_router(api_router)

def main():
    parser = argparse.ArgumentParser(description=" Restaurant Marketing Agent Command Line Interface")
    parser.add_argument(
        "--mode", 
        choices=["listen", "analyze", "draft", "campaign", "publish", "full", "realtime", "api"], 
        default="full",
        help="Pipeline execution mode (Choose 'api' to launch the web dashboard server)"
    )
    parser.add_argument(
        "--model-config",
        choices=["gemini_config", "claude_config", "ollama_config", "openai_config"],
        default="gemini_config",
        help="Agent model configuration to use"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=POLLING_INTERVAL_SECONDS,
        help="Polling interval in seconds for real-time mode"
    )
    parser.add_argument(
        "--campaign-name",
        default="Loyal Customer Weekend Promo",
        help="Name of campaign (for campaign mode)"
    )
    parser.add_argument(
        "--campaign-goal",
        default="Promote the new weekend pizza deal and offer 20% off delivery",
        help="Campaign marketing goal (for campaign mode)"
    )
    # Port configuration flag specifically for serving the web app API
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the FastAPI Uvicorn server on (default: 8000)"
    )

    args = parser.parse_args()

    if args.mode == "api":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", args.port))
        logger.info(f"Starting web dashboard API server on http://{host}:{port}")
        # Note: We pass the application reference as a string sequence to safely support hot-reloading
        uvicorn.run("main:app", host=host, port=port, reload=True)
        return

    # Initialize AgentScope models (Only runs if running in an explicit CLI workflow)
    config_path = os.path.join("config", "model_config.json")
    try:
        logger.info(f"Initializing AgentScope with configurations from: {config_path}")
        agentscope.init(model_configs=config_path)
    except Exception as e:
        logger.error(f"Failed to initialize AgentScope: {e}")
        logger.warning("Proceeding without full LLM capabilities (fallback rule-based mode will be used).")

    # Run correct CLI mode workflow
    if args.mode == "listen":
        run_listening_pipeline()
    elif args.mode == "analyze":
        run_analysis_pipeline(model_config=args.model_config)
    elif args.mode == "draft":
        insights = run_analysis_pipeline(model_config=args.model_config)
        from pipelines.content_pipeline import generate_draft_content
        generate_draft_content(insights, model_config=args.model_config)
    elif args.mode == "campaign":
        run_retention_campaign(
            campaign_name=args.campaign_name,
            goal=args.campaign_goal,
            model_config=args.model_config
        )
    elif args.mode == "publish":
        run_publishing_cycle(model_config=args.model_config)
    elif args.mode == "full":
        run_full_listening_and_insights_pipeline(model_config=args.model_config)
    elif args.mode == "realtime":
        start_realtime_listener(interval_seconds=args.interval, model_config=args.model_config)

if __name__ == "__main__":
    main()