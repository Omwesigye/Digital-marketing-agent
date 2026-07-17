import json
from schemas.data_models import Insight
from utils.logger import get_logger

logger = get_logger("insights_tools")

class InsightSynthesizer:
    def __init__(self, model_agent=None):
        self.model_agent = model_agent

    def synthesize_holistic_insights(self, sentiment_results: list, competitor_insights: list, trend_signals: list) -> list:
        """
        Synthesizes multi-dimensional data (sentiments, competitor gaps, local trends)
        into highly actionable operational and marketing insights.
        """
        if not self.model_agent:
            logger.warning("No LLM agent provided for insights synthesis.")
            return []

        # 1. Aggregate Sentiment Data
        sentiment_summary = {
            "total_analyzed": len(sentiment_results),
            "positive": sum(1 for r in sentiment_results if r.sentiment_label == "positive"),
            "negative": sum(1 for r in sentiment_results if r.sentiment_label == "negative"),
            "urgent_alerts": sum(1 for r in sentiment_results if r.is_urgent)
        }
        
        needs = []
        for r in sentiment_results:
            needs.extend(r.customer_needs)
        top_needs = list(set(needs))[:5]

        # 2. Aggregate Competitor Gaps
        competitor_weaknesses = []
        for comp in competitor_insights:
            if hasattr(comp, 'details') and 'weaknesses' in comp.details:
                competitor_weaknesses.extend(comp.details['weaknesses'])
        competitor_weaknesses = list(set(competitor_weaknesses))

        # 3. Aggregate Google Trends/News
        trending_topics = [t.content for t in trend_signals if getattr(t, 'platform', '') == 'google_trends']

        # 4. Build the Holistic Prompt
        synthesis_prompt = (
            f"As an elite restaurant marketing AI, synthesize the following multi-dimensional data:\n\n"
            f"1. Customer Sentiment: {json.dumps(sentiment_summary)}\n"
            f"2. Top Customer Needs: {top_needs}\n"
            f"3. Competitor Weaknesses (Opportunities): {competitor_weaknesses}\n"
            f"4. Trending Topics in Area: {trending_topics}\n\n"
            f"Generate exactly 2 concrete insights. One MUST be an 'operational' insight, and one MUST be a 'marketing' campaign opportunity.\n"
            f"Return a JSON array of objects with keys: 'insight_type' (str), 'title' (str), 'description' (str), and 'action_items' (list of str)."
        )

        try:
            from agentscope.message import Msg
            response = self.model_agent(Msg(name="system", content=synthesis_prompt, role="system"))
            
            raw_content = response.content.strip()
            if raw_content.startswith("```"):
                lines = raw_content.splitlines()
                if len(lines) > 2:
                    raw_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
            
            data_list = json.loads(raw_content)
            
            insights = []
            for data in data_list:
                insight = Insight(
                    insight_type=data.get("insight_type", "recommendation"),
                    title=data.get("title", "Insight"),
                    description=data.get("description", ""),
                    action_items=data.get("action_items", []),
                    confidence=0.95
                )
                insights.append(insight)
            return insights

        except Exception as e:
            logger.error(f"Failed to synthesize insights: {e}")
            return []
