import sys
import os
from unittest.mock import MagicMock

# Mock third-party dependencies that couldn't be installed
sys.modules['requests'] = MagicMock()
sys.modules['feedparser'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['apify_client'] = MagicMock()
sys.modules['pytrends'] = MagicMock()
sys.modules['pytrends.request'] = MagicMock()
sys.modules['agentscope'] = MagicMock()
sys.modules['agentscope.message'] = MagicMock()
sys.modules['agentscope.pipeline'] = MagicMock()
sys.modules['agentscope.agents'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.logging'] = MagicMock()

tenacity_mock = MagicMock()
tenacity_mock.retry = lambda *args, **kwargs: lambda f: f
tenacity_mock.stop_after_attempt = MagicMock()
tenacity_mock.wait_exponential = MagicMock()
sys.modules['tenacity'] = tenacity_mock

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

# Since pydantic might not be installed, mock the base classes enough to load schemas
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

supabase_mock = MagicMock()
sys.modules['supabase'] = supabase_mock

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipelines.data_pipeline import DataPipeline

class MockApifyTools:
    def fetch_google_trends(self, keywords):
        return [{"platform": "google_trends", "topic": "test", "trend_score": 100}]
    
    def fetch_local_news(self):
        return [{"platform": "news", "title": "test news", "content": "news content", "source_url": "http://test"}]
    
    def fetch_weather(self, city):
        return {"platform": "weather", "city": city, "temperature": 25, "condition": "Sunny", "humidity": 50}

    def fetch_x_data(self, query):
        return [{"platform": "x", "content": "test x tweet", "author": "user1", "engagement": 10}]
    
    def fetch_tiktok_data(self, query):
        return []

    def fetch_instagram_hashtags(self, hashtag):
        return []
    
    def fetch_google_reviews(self, target):
        return []

class MockSupabaseService:
    def insert_signals(self, signals):
        print(f"Mock DB Insert: {len(signals)} signals inserted.")
        return [f"mock-id-{i}" for i in range(len(signals))]

def run_test():
    print("Initializing DataPipeline...")
    pipeline = DataPipeline()
    
    # Inject mocks
    pipeline.collector = MockApifyTools()
    pipeline.db_service = MockSupabaseService()
    
    # Run the ETL
    print("Running ETL...")
    inserted_ids = pipeline.run()
    
    print(f"Test Successful! Inserted IDs: {inserted_ids}")

if __name__ == "__main__":
    run_test()
