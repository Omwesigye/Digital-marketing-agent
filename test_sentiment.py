import sys
import os
import json
from unittest.mock import MagicMock

# 1. Mock dependencies that might be missing locally
sys.modules['agentscope'] = MagicMock()
sys.modules['agentscope.agents'] = MagicMock()
sys.modules['agentscope.message'] = MagicMock()
sys.modules['pytrends'] = MagicMock()
sys.modules['apify_client'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

# Mock Supabase
sys.modules['supabase'] = MagicMock()

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

# Since we want to test VADER + our Analyzer, let's ensure vaderSentiment is available
try:
    import vaderSentiment
except ImportError:
    # If missing locally, mock VADER to simulate the NLP engine
    vader_mock = MagicMock()
    analyzer_mock = MagicMock()
    analyzer_mock.polarity_scores.return_value = {"compound": -0.8}
    vader_mock.SentimentIntensityAnalyzer = lambda: analyzer_mock
    sys.modules['vaderSentiment'] = vader_mock
    sys.modules['vaderSentiment.vaderSentiment'] = vader_mock

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.sentiment_tools import SentimentAnalyzer

# 2. Create a Mock LLM Agent
class MockSentimentAgent:
    def __call__(self, msg):
        # We simulate the LLM analyzing the text and returning structured JSON
        simulated_llm_response = {
            "sentiment_label": "negative",
            "sentiment_score": -0.85,
            "emotions": {
                "anger": 0.9,
                "disappointment": 0.8,
                "joy": 0.0
            },
            "key_phrases": ["waited an hour", "cold food", "terrible service"],
            "customer_needs": ["faster delivery", "better temperature control", "apology/refund"],
            "is_urgent": True
        }
        
        # Mock the AgentScope response object
        response_mock = MagicMock()
        response_mock.content = json.dumps(simulated_llm_response)
        return response_mock

def test_sentiment_pipeline():
    print("Initializing Hybrid Sentiment Analyzer (NLP + LLM)...")
    
    # We pass our mock LLM agent to the analyzer
    mock_agent = MockSentimentAgent()
    analyzer = SentimentAnalyzer(model_agent=mock_agent)
    
    # 3. Define a sample customer review
    sample_text = "I waited for over an hour to get my pizza. When it finally arrived, it was completely cold and tasted terrible! I demand a refund immediately, this is the worst service ever."
    print(f"\n--- Analyzing Customer Review ---\nText: '{sample_text}'\n")
    
    # 4. Run Analysis
    result = analyzer.analyze_text(signal_id="test_signal_123", text=sample_text)
    
    # 5. Output results
    print("--- Final Analysis Output ---")
    print(f"Sentiment Label : {result.sentiment_label.upper()}")
    print(f"Sentiment Score : {result.sentiment_score}")
    print(f"Emotions        : {result.emotions}")
    print(f"Key Phrases     : {result.key_phrases}")
    print(f"Customer Needs  : {result.customer_needs}")
    print(f"Is Urgent?      : {'YES - FLAG FOR ACTION' if result.is_urgent else 'No'}")

if __name__ == "__main__":
    test_sentiment_pipeline()
