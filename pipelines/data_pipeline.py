from tools.apify_tools import ApifyTools
from tools.data_cleaner import DataCleaner
from services.supabase_service import SupabaseService
from utils.logger import get_logger
import datetime

logger = get_logger("data_pipeline")

class DataPipeline:
    def __init__(self):
        self.collector = ApifyTools()
        self.cleaner = DataCleaner()
        self.db_service = SupabaseService()

    def extract(self) -> dict:
        """
        [E]xtract phase: Fetches raw data from all active scrapers/APIs.
        Each source is isolated so that a single failure doesn't halt extraction.
        """
        logger.info("Starting raw data EXTRACTION phase...")
        extracted_data = {}
        
        # 1. Google Trends
        try:
            from config.sources import get_google_trends_keywords
            extracted_data["google_trends"] = self.collector.fetch_google_trends(get_google_trends_keywords())
        except Exception as e:
            logger.error(f"Extraction failed for Google Trends: {e}")
            extracted_data["google_trends"] = []

        # 2. Local News
        try:
            extracted_data["news"] = self.collector.fetch_local_news()
        except Exception as e:
            logger.error(f"Extraction failed for Local News: {e}")
            extracted_data["news"] = []

        # 3. Weather
        try:
            from config.sources import get_weather_cities
            weather_data = []
            for city in get_weather_cities():
                w = self.collector.fetch_weather(city=city)
                if w:
                    weather_data.append(w)
            extracted_data["weather"] = weather_data
        except Exception as e:
            logger.error(f"Extraction failed for Weather API: {e}")
            extracted_data["weather"] = []

        # 4. Apify Sources (X, TikTok, Instagram, Google Reviews)
        apify_sources = [
            ("x", self.collector.fetch_x_data, "get_twitter_queries"),
            ("tiktok", self.collector.fetch_tiktok_data, "get_tiktok_queries"),
            ("instagram", self.collector.fetch_instagram_hashtags, "get_instagram_hashtags"),
            ("google_reviews", self.collector.fetch_google_reviews, "get_google_reviews_targets")
        ]

        for platform, fetch_fn, config_fn_name in apify_sources:
            try:
                import config.sources as src
                config_fn = getattr(src, config_fn_name)
                extracted_data[platform] = []
                for query in config_fn():
                    extracted_data[platform].extend(fetch_fn(query))
            except Exception as e:
                logger.error(f"Extraction failed for {platform}: {e}")
                extracted_data[platform] = []

        # Convert any Pydantic objects to dicts
        for platform, items in extracted_data.items():
            dict_items = []
            for item in items:
                if hasattr(item, "dict"):
                    dict_items.append(item.dict())
                else:
                    dict_items.append(item)
            extracted_data[platform] = dict_items

        return extracted_data

    def transform(self, raw_data: dict) -> list:
        """
        [T]ransform phase: Cleans and validates inputs against schemas.
        """
        logger.info("Starting data TRANSFORMATION phase...")
        cleaned_signals = self.cleaner.clean_and_validate(raw_data)
        logger.info(f"Transformed raw payloads into {len(cleaned_signals)} valid RawSignals.")
        return cleaned_signals

    def load(self, signals: list) -> list:
        """
        [L]oad phase: Persists data to the Supabase database and local audit CSV.
        """
        logger.info("Starting data LOAD phase...")
        if not signals:
            logger.warning("No signal data to load.")
            return []

        # Backup save to CSV
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.cleaner.save_to_csv(signals, filename=f"raw_signals_{timestamp_str}.csv")

        # Load to DB
        inserted_ids = self.db_service.insert_signals(signals)
        logger.info(f"Loaded {len(inserted_ids)} records to database.")
        return inserted_ids

    def run(self) -> list:
        """
        Executes the ETL loop end-to-end.
        """
        raw_data = self.extract()
        transformed_signals = self.transform(raw_data)
        inserted_ids = self.load(transformed_signals)
        return inserted_ids