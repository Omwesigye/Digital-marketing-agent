import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from schemas.data_models import SentimentResult
from utils.logger import get_logger

logger = get_logger("sentiment_tools")

class SentimentAnalyzer:
    def __init__(self, model_agent=None):
        self.vader = SentimentIntensityAnalyzer()
        self.model_agent = model_agent  # Optionally pass an AgentScope agent for deep LLM analysis

    def analyze_text(self, signal_id: str, text: str) -> SentimentResult:
        """
        Runs sentiment analysis on text.
        Uses VADER for fast polarity analysis, and uses the LLM if provided for deep feature extraction.
        """
        # 1. Fast VADER analysis
        scores = self.vader.polarity_scores(text)
        compound = scores["compound"]

        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"

        # 2. Extract emotions & needs (heuristics as fallback)
        emotions = {"joy": 0.0, "anger": 0.0, "disappointment": 0.0, "surprise": 0.0}
        key_phrases = []
        customer_needs = []
        is_urgent = False

        if label == "negative":
            emotions["disappointment"] = 0.7
            if any(word in text.lower() for word in ["slow", "waiting", "delay", "late"]):
                customer_needs.append("faster service/delivery")
            if any(word in text.lower() for word in ["cold", "bad", "tasteless", "burnt"]):
                customer_needs.append("better food quality control")
            if any(word in text.lower() for word in ["rude", "worst", "terrible", "hate"]):
                is_urgent = True
                emotions["anger"] = 0.8
        elif label == "positive":
            emotions["joy"] = 0.8
            if any(word in text.lower() for word in ["love", "best", "delicious", "amazing"]):
                key_phrases.append("positive customer feedback")

        # 3. Enhance with LLM agent if configured
        if self.model_agent:
            try:
                from agentscope.message import Msg
                prompt = (
                    f"Analyze this content for a restaurant:\n"
                    f"\"{text}\"\n"
                    f"Return a JSON response conforming to the schema specified in your instructions."
                )
                response = self.model_agent(Msg(name="system", content=prompt, role="system"))
                
                # Try parsing LLM JSON output
                raw_content = response.content.strip()
                # Strip markdown code blocks if any
                if raw_content.startswith("```"):
                    lines = raw_content.splitlines()
                    if len(lines) > 2:
                        raw_content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
                
                data = json.loads(raw_content)
                label = data.get("sentiment_label", label)
                compound = data.get("sentiment_score", compound)
                emotions = data.get("emotions", emotions)
                key_phrases = data.get("key_phrases", key_phrases)
                customer_needs = data.get("customer_needs", customer_needs)
                is_urgent = data.get("is_urgent", is_urgent)
            except Exception as e:
                logger.error(f"Failed to enhance sentiment with LLM agent: {e}. Falling back to rule-based.")

        return SentimentResult(
            signal_id=signal_id,
            sentiment_label=label,
            sentiment_score=compound,
            emotions=emotions,
            key_phrases=key_phrases,
            customer_needs=customer_needs,
            is_urgent=is_urgent
        )
