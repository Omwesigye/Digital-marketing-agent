from fastapi import APIRouter, BackgroundTasks, HTTPException
import asyncio

router = APIRouter(prefix="/api")

# In-memory global state placeholder for pipeline status tracking
pipeline_state = {"status": "idle", "last_run": None, "continuous": False}

continuous_task = None

async def run_full_pipeline_cycle():
    """Executes the full extraction and analysis cycle."""
    global pipeline_state
    pipeline_state["status"] = "processing"
    
    try:
        from pipelines.master_pipeline import run_full_listening_and_insights_pipeline
        # Run the full pipeline (Extract, Transform, Analyze, Draft)
        await asyncio.to_thread(run_full_listening_and_insights_pipeline)
    except Exception as e:
        print(f"Pipeline error: {e}")
        
    pipeline_state["status"] = "idle"

async def continuous_pipeline_worker():
    """Loops continuously with a delay between cycles."""
    global pipeline_state
    while pipeline_state["continuous"]:
        await run_full_pipeline_cycle()
        # Wait 15 minutes before the next scrape
        if pipeline_state["continuous"]:
            pipeline_state["status"] = "sleeping"
            await asyncio.sleep(15 * 60)

@router.get("/insights")
async def get_insights():
    return [
        {"id": 1, "metric": "Foot Traffic", "change": "+14%", "recommendation": "Launch a Tuesday taco special to optimize low-volume hours."},
        {"id": 2, "metric": "Review Sentiment", "change": "-4% Yelp", "recommendation": "Address complaints regarding delivery times by automating text notifications."}
    ]

@router.get("/drafts")
async def get_drafts():
    try:
        from services.supabase_service import SupabaseService
        db = SupabaseService()
        if db.is_available():
            res = db.client.table("content_library").select("*").eq("status", "draft").execute()
            if res.data:
                return res.data
    except Exception as e:
        print(f"Failed to fetch drafts from DB: {e}")
        
    # Fallback mock data
    return [
        {"id": 101, "platform": "instagram", "title": "[REEL] Fresh Pizza", "body": "Craving something savory? Our signature wood-fired pizza is fresh out of the oven! 🍕 #LocalEats", "status": "draft"},
        {"id": 102, "platform": "x", "title": "[FLIER] Happy Hour", "body": "Join us for Happy Hour this Thursday! Half off all premium drafts from 4 PM - 7 PM. 🍻", "status": "draft"},
        {"id": 103, "platform": "tiktok", "title": "[SOUNDTRACK] Trending Audio", "body": "Soundtrack: Trending Lofi Beat. Captions: POV you found the best pizza spot in town.", "status": "draft"},
        {"id": 104, "platform": "email", "title": "[DRAFT EMAIL] Special Offer for Valued Guest", "body": "Hi there,\n\nWe noticed you haven't visited in a while! Here is 20% off your next delivery order.", "status": "draft"}
    ]

@router.get("/competitors")
async def get_competitors():
    return [
        {"id": 1, "name": "Pizza Hut", "move": "Launched $5 value menu", "threat_level": "High", "action": "Counter with local loyalty discounts."},
        {"id": 2, "name": "Domino's", "move": "Extended late-night delivery hours", "threat_level": "Medium", "action": "Highlight our faster average delivery times in targeted ads."}
    ]

@router.get("/sentiment")
async def get_sentiment():
    return {
        "overall_score": 8.4,
        "emotions": [
            {"name": "Joy", "value": 65, "color": "#4caf50"},
            {"name": "Surprise", "value": 20, "color": "#2196f3"},
            {"name": "Frustration", "value": 10, "color": "#f44336"},
            {"name": "Sadness", "value": 5, "color": "#9e9e9e"}
        ],
        "recent_feedback": [
            {"text": "Best pizza in town!", "emotion": "Joy"},
            {"text": "Delivery took too long on Friday.", "emotion": "Frustration"}
        ]
    }

@router.get("/retention")
async def get_retention():
    return {
        "churn_risk": "Medium",
        "active_campaigns": 2,
        "metrics": [
            {"label": "Repeat Customers", "value": "42%", "trend": "+2%"},
            {"label": "Avg Lifetime Value", "value": "$350", "trend": "+$15"}
        ],
        "suggested_actions": [
            "Send 'We Miss You' 20% off coupon to users inactive for 30+ days.",
            "Enroll top 10% spenders in VIP loyalty program."
        ]
    }

@router.post("/pipeline/start")
async def trigger_pipeline(background_tasks: BackgroundTasks):
    global pipeline_state
    if pipeline_state["status"] == "processing":
        raise HTTPException(status_code=400, detail="Pipeline is already running.")
        
    background_tasks.add_task(run_full_pipeline_cycle)
    return {"status": "started", "message": "AgentScope pipeline processing asynchronously."}

@router.post("/pipeline/start_continuous")
async def start_continuous(background_tasks: BackgroundTasks):
    global pipeline_state
    if pipeline_state["continuous"]:
        return {"status": "already_running"}
    
    pipeline_state["continuous"] = True
    background_tasks.add_task(continuous_pipeline_worker)
    return {"status": "started", "message": "Continuous scraping mode activated."}

@router.post("/pipeline/stop_continuous")
async def stop_continuous():
    global pipeline_state
    pipeline_state["continuous"] = False
    if pipeline_state["status"] == "sleeping":
        pipeline_state["status"] = "idle"
    return {"status": "stopped", "message": "Continuous mode deactivated."}

@router.get("/pipeline/status")
async def get_pipeline_status():
    return pipeline_state