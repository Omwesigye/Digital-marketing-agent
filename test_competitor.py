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

from tools.competitor_tools import CompetitorAnalyzer

# Create a Mock LLM Agent
class MockCompetitorAgent:
    def __call__(self, msg):
        simulated_llm_response = {
            "strengths": ["Great ambience", "Friendly staff", "Generous portions"],
            "weaknesses": ["Slow service during peak hours", "Limited vegetarian options"],
            "tactics": ["Focusing on family dining weekends"]
        }
        response_mock = MagicMock()
        response_mock.content = json.dumps(simulated_llm_response)
        return response_mock

def test_competitor_aggregation():
    print("Initializing Competitor Analyzer...")
    
    analyzer = CompetitorAnalyzer(model_agent=MockCompetitorAgent())
    
    # Define sample raw signals (Google Reviews) for a single competitor
    mock_signals = [
        {"author": "Luigi's Pizza", "content": "The pizza was huge and tasted great, but we waited 45 minutes for a table.", "engagement": 4},
        {"author": "Luigi's Pizza", "content": "Awesome family spot! Kids loved it. Friendly waiters.", "engagement": 5},
        {"author": "Luigi's Pizza", "content": "Very slow service and absolutely no vegan options on the menu.", "engagement": 2},
        {"author": "Burger Joint", "content": "Best burgers in town but super greasy.", "engagement": 4}
    ]
    
    print(f"\n--- Processing {len(mock_signals)} Reviews ---\n")
    
    # Run Analysis
    insights = analyzer.aggregate_and_analyze(signals=mock_signals)
    
    # Output results
    for insight in insights:
        print("========================================")
        print(f"Competitor: {insight.competitor_name}")
        print(f"Aggregated Rating: {insight.metric_value}/5.0 based on {insight.details['review_count']} reviews")
        print(f"Strengths: {insight.details['strengths']}")
        print(f"Weaknesses: {insight.details['weaknesses']}")
        print(f"Detected Tactics: {insight.details['tactics']}")
        print("========================================\n")

if __name__ == "__main__":
    test_competitor_aggregation()
