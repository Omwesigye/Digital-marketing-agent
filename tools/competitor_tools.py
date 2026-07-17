import json
from collections import defaultdict
from schemas.data_models import CompetitorInsight
from utils.logger import get_logger

logger = get_logger("competitor_tools")

class CompetitorAnalyzer:
    def __init__(self, model_agent=None):
        self.model_agent = model_agent

    def aggregate_and_analyze(self, signals: list) -> list:
        """
        Groups raw signals (reviews) by competitor and asks the LLM
        to synthesize aggregated strengths and weaknesses.
        """
        # 1. Group reviews by competitor
        competitor_reviews = defaultdict(list)
        for sig in signals:
            comp_name = sig.get("author") or "Unknown Competitor"
            content = sig.get("content") or ""
            rating = sig.get("engagement") or 0
            competitor_reviews[comp_name].append({"content": content, "rating": rating})

        insights = []

        # 2. Analyze each competitor in aggregate
        for comp_name, reviews in competitor_reviews.items():
            if not self.model_agent:
                logger.warning("No LLM agent provided for competitor analysis.")
                continue

            # Calculate average rating
            avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0

            # Prepare batch prompt
            reviews_text = "\n".join([f"- Rating: {r['rating']} | Review: {r['content']}" for r in reviews])
            prompt = (
                f"Analyze these {len(reviews)} reviews for competitor '{comp_name}':\n"
                f"{reviews_text}\n\n"
                f"Extract the overall strengths, weaknesses, and marketing tactics as a JSON object with keys: "
                f"'strengths' (list of str), 'weaknesses' (list of str), 'tactics' (list of str)."
            )

            try:
                from agentscope.message import Msg
                response = self.model_agent(Msg(name="system", content=prompt, role="system"))
                
                raw_content = response.content.strip()
                if raw_content.startswith("```"):
                    lines = raw_content.splitlines()
                    if len(lines) > 2:
                        raw_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
                
                data = json.loads(raw_content)

                insight = CompetitorInsight(
                    competitor_name=comp_name,
                    platform="google_reviews",
                    metric_type="aggregated_sentiment",
                    metric_value=avg_rating,
                    details={
                        "strengths": data.get("strengths", []),
                        "weaknesses": data.get("weaknesses", []),
                        "tactics": data.get("tactics", []),
                        "review_count": len(reviews)
                    }
                )
                insights.append(insight)
            except Exception as e:
                logger.error(f"Failed to analyze competitor {comp_name}: {e}")

        return insights
