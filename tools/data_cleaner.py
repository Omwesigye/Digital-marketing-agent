import csv
import os
from datetime import datetime
from schemas.data_models import RawSignal
from utils.logger import get_logger

logger = get_logger("data_cleaner")

class DataCleaner:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()

    def clean_and_validate(self, raw_data: dict) -> list:
        """
        Parses raw multi-source data and cleans it into a list of RawSignal models.
        Handles schemas for weather, trends, news, social media, and reviews.
        """
        cleaned_signals = []

        for platform, items in raw_data.items():
            if not items:
                continue

            # Ensure items is always a list (just in case weather is passed as dict)
            if not isinstance(items, list):
                items = [items]

            for item in items:
                try:
                    content = ""
                    author = "anonymous"
                    source_url = ""
                    engagement = 0
                    metadata = item.copy()

                    if platform in ["x", "tiktok", "instagram"]:
                        content = item.get("caption") or item.get("content") or ""
                        author = item.get("author") or "anonymous"
                        source_url = item.get("source_url") or ""
                        engagement = int(item.get("engagement_likes") or item.get("engagement") or 0)

                    elif platform == "google_reviews":
                        content = item.get("text") or item.get("review_text") or ""
                        author = item.get("author") or item.get("competitor_name") or "anonymous"
                        # Use competitor name as author to track where the review belongs
                        engagement = int(item.get("rating") or 0)  # Use engagement to store rating for easy filtering

                    elif platform == "google_trends":
                        content = f"Trend topic: {item.get('topic')} (score: {item.get('trend_score')})"
                        author = "google_trends"
                        engagement = int(item.get("trend_score") or 0)

                    elif platform == "news":
                        content = f"{item.get('title')}: {item.get('content')}"
                        author = "local_news"
                        source_url = item.get("source_url") or ""

                    elif platform == "weather":
                        content = f"Weather in {item.get('city')}: Temp: {item.get('temperature')}C, Condition: {item.get('condition')}, Humidity: {item.get('humidity')}%"
                        author = item.get("city") or "weather_api"

                    # Skip empty signals
                    if not content.strip():
                        continue

                    # Create and validate RawSignal model
                    signal = RawSignal(
                        platform=platform,
                        content=content,
                        author=author,
                        source_url=source_url,
                        engagement=engagement,
                        raw_metadata=metadata,
                        scraped_at=datetime.fromisoformat(self.timestamp)
                    )
                    cleaned_signals.append(signal)

                except Exception as e:
                    logger.error(f"Failed parsing item from platform {platform}: {e}. Item: {item}")

        return cleaned_signals

    def save_to_csv(self, signals: list, filename: str = "raw_dataset.csv", directory: str = "data/raw"):
        """Saves a list of RawSignal models to a CSV file."""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)

        if not signals:
            logger.warning("No signals to save to CSV.")
            return

        # Get header keys from the first object
        first_signal = signals[0]
        keys = first_signal.dict().keys() if hasattr(first_signal, "dict") else first_signal.keys()

        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for sig in signals:
                    row = sig.dict() if hasattr(sig, "dict") else sig
                    # Convert dicts/lists to string for CSV compatibility
                    if "raw_metadata" in row and isinstance(row["raw_metadata"], dict):
                        import json
                        row["raw_metadata"] = json.dumps(row["raw_metadata"])
                    writer.writerow(row)
            logger.info(f"Saved cleaned signals to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")