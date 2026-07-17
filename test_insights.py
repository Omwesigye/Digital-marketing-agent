import sys
import os
import json
from unittest.mock import MagicMock

# Mock dependencies
sys.modules['agentscope'] = MagicMock()
sys.modules['agentscope.agents'] = MagicMock()
sys.modules['agentscope.message'] = MagicMock()

# Mock Pydantic
pydantic_mock = MagicMock()
class BaseModelMock:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    def dict(self):
        return self.__dict__
pydantic_mock.BaseModel = BaseModelMock
pydantic_mock.Field = lambda default_factory=None: None
pydantic_mock.EmailStr = str
sys.modules['pydantic'] = pydantic_mock

# Mock Logger
import logging
logger_mock = MagicMock()
def get_logger(name):
    l = logging.getLogger(name)
    l.setLevel(logging.INFO)
    if not l.handlers:
        l.addHandler(logging.StreamHandler(sys.stdout))
    return l
logger_mock.get_logger = get_logger
sys.modules['utils.logger'] = logger_mock

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.insights_tools import InsightSynthesizer
from schemas.data_models import SentimentResult, CompetitorInsight, RawSignal

# Create a Mock LLM Agent
class MockInsightsAgent:
    def __call__(self, msg):
        simulated_llm_response = [
            {
                "insight_type": "operational",
                "title": "Fix Temperature Control Logistics",
                "description": "5 urgent sentiment alerts complained about cold food delivery. Implement insulated delivery bags immediately.",
                "action_items": ["Audit delivery vendor bags", "Reduce prep-to-handover wait times"]
            },
            {
                "insight_type": "marketing",
                "title": "Launch 'Vegan Delight' Pizza Promo",
                "description": "Google Trends shows high interest in Vegan diets locally, and your primary competitor (Luigi's) was specifically flagged for having 'limited vegetarian options'. Capture this market gap.",
                "action_items": ["Create Instagram Reel showcasing new Vegan Pizza", "Draft email campaign to existing subscribers with 10% vegan discount"]
            }
        ]
        response_mock = MagicMock()
        response_mock.content = json.dumps(simulated_llm_response)
        return response_mock

def test_insights_synthesis():
    print("Initializing Holistic Insight Synthesizer...")
    synthesizer = InsightSynthesizer(model_agent=MockInsightsAgent())
    
    # 1. Mock Sentiment Data (Output of sentiment_pipeline)
    mock_sentiments = [
        SentimentResult(signal_id="1", sentiment_label="negative", sentiment_score=-0.8, customer_needs=["better temperature control"], is_urgent=True),
        SentimentResult(signal_id="2", sentiment_label="negative", sentiment_score=-0.7, customer_needs=["better temperature control"], is_urgent=True),
        SentimentResult(signal_id="3", sentiment_label="positive", sentiment_score=0.9, customer_needs=["vegan options"], is_urgent=False),
    ]

    # 2. Mock Competitor Data (Output of competitor_pipeline)
    mock_competitor = CompetitorInsight(
        competitor_name="Luigi's Pizza", metric_type="sentiment", metric_value=3.5,
        details={"weaknesses": ["Limited vegetarian options", "Slow delivery"]}
    )

    # 3. Mock Trend Data (Output of ETL extractor)
    mock_trends = [
        RawSignal(platform="google_trends", content="Trend topic: Vegan diets (score: 95)")
    ]

    print("\n--- Running Multi-Dimensional Synthesis ---")
    insights = synthesizer.synthesize_holistic_insights(
        sentiment_results=mock_sentiments,
        competitor_insights=[mock_competitor],
        trend_signals=mock_trends
    )
    
    # Output results
    for i, insight in enumerate(insights, 1):
        print(f"\n[ Insight #{i} - {insight.insight_type.upper()} ]")
        print(f"Title: {insight.title}")
        print(f"Description: {insight.description}")
        print("Action Items:")
        for action in getattr(insight, 'action_items', []):
            print(f"  -> {action}")

if __name__ == "__main__":
    test_insights_synthesis()
