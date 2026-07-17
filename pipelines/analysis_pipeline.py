import json
from agentscope.message import Msg

from agents.processing.sentiment_agent import build_sentiment_agent
from agents.processing.competitor_agent import build_competitor_agent
from agents.processing.insights_agent import build_insights_agent
from services.supabase_service import SupabaseService
from tools.sentiment_tools import SentimentAnalyzer
from schemas.data_models import CompetitorInsight, Insight
from utils.logger import get_logger

logger = get_logger("analysis_pipeline")

def run_analysis_pipeline(signal_ids: list = None, model_config: str = "gemini_config") -> list:
    """
    Orchestrates Phase 3:
    1. Sentiment Analysis on collected signals.
    2. Competitor intelligence synthesis.
    3. LLM-based insight & recommendation extraction.
    Persists all analytical outputs to the database.
    """
    logger.info("Starting analysis pipeline...")
    db = SupabaseService()
    
    # 1. Fetch recent signals if not provided
    if not signal_ids:
        logger.info("No signal IDs provided. Fetching last 50 signals from database.")
        signals = db.get_recent_signals(limit=50)
    else:
        # Fetch matching signals from DB
        if db.is_available():
            try:
                signals = db.client.table("raw_signals").select("*").in_("id", signal_ids).execute().data
            except Exception as e:
                logger.error(f"Failed to fetch specified signals: {e}")
                signals = []
        else:
            signals = []

    if not signals:
        logger.warning("No signals available for analysis.")
        return []

    # 2. Initialize Agents & Tools
    sentiment_agent = build_sentiment_agent(model_config)
    competitor_agent = build_competitor_agent(model_config)
    insights_agent = build_insights_agent(model_config)

    analyzer = SentimentAnalyzer(model_agent=sentiment_agent)

    # 3. Step 1: Sentiment analysis on raw signals
    logger.info(f"Analyzing sentiment for {len(signals)} signals...")
    sentiment_results = []
    competitor_raw_data = []

    for sig in signals:
        try:
            content = sig.get("content") or ""
            sig_id = sig.get("id", "mock-id")
            
            # Run sentiment analysis
            res = analyzer.analyze_text(sig_id, content)
            sentiment_results.append(res)

            # Track competitor signals separately for the competitor agent
            if sig.get("platform") == "google_reviews":
                competitor_raw_data.append(sig)

        except Exception as e:
            logger.error(f"Error analyzing signal {sig.get('id')}: {e}")

    # Save sentiments to database
    if sentiment_results:
        db.insert_sentiments(sentiment_results)
        logger.info(f"Saved {len(sentiment_results)} sentiment analysis results.")

    # 4. Step 2: Competitor analysis
    logger.info(f"Processing competitor tracking for {len(competitor_raw_data)} review signals...")
    for comp_sig in competitor_raw_data:
        try:
            # Query LLM competitor agent
            prompt = (
                f"Analyze this customer feedback for competitor tracking:\n"
                f"Review content: \"{comp_sig.get('content')}\"\n"
                f"Competitor/Place: \"{comp_sig.get('author')}\"\n"
                f"Rating given: {comp_sig.get('engagement')}\n"
                f"Extract competitor metrics, strengths, weaknesses, and tactics as JSON."
            )
            response = competitor_agent(Msg(name="system", content=prompt, role="system"))
            
            # Clean and parse JSON
            raw_content = response.content.strip()
            if raw_content.startswith("```"):
                lines = raw_content.splitlines()
                if len(lines) > 2:
                    raw_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
            
            data = json.loads(raw_content)
            
            # Save competitor insight
            comp_insight = CompetitorInsight(
                competitor_name=data.get("competitor_name") or comp_sig.get("author"),
                platform=comp_sig.get("platform"),
                metric_type="rating",
                metric_value=float(comp_sig.get("engagement") or 0),
                details=data
            )
            db.insert_competitor_insight(comp_insight)
        except Exception as e:
            logger.error(f"Failed competitor intelligence extract: {e}")

    # 5. Step 3: Synthesis & Insight recommendations
    logger.info("Running insights synthesis with message hub...")
    generated_insights = []

    # Compile a summary text of the latest data for context
    sentiment_summary = {
        "total_analyzed": len(sentiment_results),
        "positive": sum(1 for r in sentiment_results if r.sentiment_label == "positive"),
        "negative": sum(1 for r in sentiment_results if r.sentiment_label == "negative"),
        "neutral": sum(1 for r in sentiment_results if r.sentiment_label == "neutral"),
        "urgent_alerts": sum(1 for r in sentiment_results if r.is_urgent)
    }

    recent_needs = []
    for r in sentiment_results:
        recent_needs.extend(r.customer_needs)
    # Deduplicate needs
    recent_needs = list(set(recent_needs))[:10]

    synthesis_prompt = (
        f"Aggregated Listening Data:\n"
        f"- Sentiment summary: {json.dumps(sentiment_summary)}\n"
        f"- Detected customer needs: {recent_needs}\n"
        f"Generate a concrete marketing/operational insight recommendation for the restaurant."
    )

    try:
        response = insights_agent(Msg(name="system", content=synthesis_prompt, role="system"))
        
        raw_content = response.content.strip()
        if raw_content.startswith("```"):
            lines = raw_content.splitlines()
            if len(lines) > 2:
                raw_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
        
        data = json.loads(raw_content)
        
        # Save insight to DB
        insight = Insight(
            insight_type=data.get("insight_type") or "recommendation",
            title=data.get("title") or "Dynamic Restaurant Recommendation",
            description=data.get("description") or response.content,
            confidence=float(data.get("confidence") or 1.0),
            data_sources=signal_ids or [],
            action_items=data.get("action_items") or []
        )
        insight_id = db.insert_insight(insight)
        # Attach ID to the returned dictionary for down-pipeline steps
        insight_dict = insight.dict()
        insight_dict["id"] = insight_id
        generated_insights.append(insight_dict)
        logger.info(f"Insight generated successfully: \"{insight.title}\"")
    except Exception as e:
        logger.error(f"Failed to generate insight: {e}")

    logger.info("Analysis pipeline complete ✔")
    return generated_insights
