import os
import re
import requests
import feedparser

from dotenv import load_dotenv
from apify_client import ApifyClient
from pytrends.request import TrendReq
from datetime import datetime

from config.sources import (
    get_twitter_queries,
    get_tiktok_queries,
    get_instagram_hashtags,
    get_google_reviews_targets,
    get_google_trends_keywords,
    get_news_feeds,
    get_weather_cities
)

from utils.etl_helpers import with_retry, disk_cache
from schemas.etl_models import Post, Review, WeatherData, Profile

load_dotenv()


class ApifyTools:
    def __init__(self):
        token = os.getenv("APIFY_TOKEN")

        self.client = ApifyClient(token) if token else None
        self.pytrend = TrendReq(
            hl="en-US",
            tz=180
        )

    # ==========================================================
    # COMMON NORMALIZATION
    # ==========================================================

    def _normalize_text(self, text: str) -> str:
        """
        Removes URLs, hashtags and excessive whitespace.
        """
        if not text:
            return ""

        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        text = re.sub(r"#[A-Za-z0-9_]+", "", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ==========================================================
    # X / TWITTER
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=6)
    def fetch_x_data(self, query: str, limit: int = 15) -> list[Post]:
        if not self.client:
            return []

        try:
            run = self.client.actor("apidojo/twitter-scraper-lite").call(
                run_input={
                    "searchTerms": [query],
                    "maxItems": limit
                }
            )

            cleaned_records = []
            dataset_id = run["defaultDatasetId"] if isinstance(run, dict) else run.default_dataset_id
            for item in self.client.dataset(dataset_id).iterate_items():
                parsed_content = self._normalize_text(item.get("text", ""))
                if not parsed_content:
                    continue

                post = Post(
                    platform="x",
                    id=str(item.get("id", "")),
                    author=item.get("twitterUrl", "").split("/")[-1] or "anonymous",
                    caption=parsed_content,
                    source_url=item.get("url"),
                    engagement_likes=int(item.get("likeCount", 0)),
                    engagement_shares=int(item.get("retweetCount", 0))
                )
                cleaned_records.append(post)

            return cleaned_records
        except Exception as e:
            print(f"[X] {e}")
            return []

    # ==========================================================
    # TIKTOK
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=6)
    def fetch_tiktok_data(self, query: str, limit: int = 10) -> list[Post]:
        if not self.client:
            return []

        try:
            run = self.client.actor("clockworks/tiktok-scraper").call(
                run_input={
                    "search": [query],
                    "resultsPerPage": limit
                }
            )

            cleaned_records = []
            dataset_id = run["defaultDatasetId"] if isinstance(run, dict) else run.default_dataset_id
            for item in self.client.dataset(dataset_id).iterate_items():
                parsed_content = self._normalize_text(item.get("text", ""))
                if not parsed_content:
                    continue

                post = Post(
                    platform="tiktok",
                    id=str(item.get("id", "")),
                    author=item.get("authorMeta", {}).get("name", "anonymous"),
                    caption=parsed_content,
                    source_url=item.get("webVideoUrl"),
                    engagement_likes=int(item.get("diggCount", 0)),
                    engagement_shares=int(item.get("shareCount", 0)),
                    engagement_comments=int(item.get("commentCount", 0)),
                )
                cleaned_records.append(post)

            return cleaned_records
        except Exception as e:
            print(f"[TikTok] {e}")
            return []

    # ==========================================================
    # INSTAGRAM
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=6)
    def fetch_instagram_hashtags(self, hashtag: str, limit: int = 20) -> list[Post]:
        if not self.client:
            return []

        try:
            run = self.client.actor("apify/instagram-hashtag-scraper").call(
                run_input={
                    "hashtags": [hashtag],
                    "resultsLimit": limit
                }
            )

            posts = []
            dataset_id = run["defaultDatasetId"] if isinstance(run, dict) else run.default_dataset_id
            for item in self.client.dataset(dataset_id).iterate_items():
                text = self._normalize_text(item.get("caption", ""))
                if not text:
                    continue

                post = Post(
                    platform="instagram",
                    id=str(item.get("id", "")),
                    author=item.get("ownerUsername", "anonymous"),
                    caption=text,
                    source_url=item.get("url"),
                    engagement_likes=int(item.get("likesCount", 0)),
                    engagement_comments=int(item.get("commentsCount", 0))
                )
                posts.append(post)

            return posts
        except Exception as e:
            print(f"[Instagram] {e}")
            return []

    # ==========================================================
    # GOOGLE REVIEWS
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=12)
    def fetch_google_reviews(self, search_term: str, max_reviews: int = 5) -> list[Review]:
        if not self.client:
            return []

        try:
            run = self.client.actor("compass/crawler-google-places").call(
                run_input={
                    "searchStringsArray": [search_term],
                    "maxReviews": max_reviews,
                    "language": "en"
                }
            )

            cleaned_reviews = []
            dataset_id = run["defaultDatasetId"] if isinstance(run, dict) else run.default_dataset_id
            for item in self.client.dataset(dataset_id).iterate_items():
                reviews = item.get("reviews", [])
                competitor_name = item.get("title", search_term)

                if not reviews and item.get("text"):
                    reviews = [item]

                for review in reviews:
                    parsed_text = self._normalize_text(review.get("text", ""))
                    rating = float(review.get("stars", review.get("rating", 0)))
                    
                    r = Review(
                        platform="google_reviews",
                        author=review.get("name", "anonymous"),
                        rating=rating,
                        text=parsed_text if parsed_text else f"[Rating Only: {rating}] - {competitor_name}"
                    )
                    cleaned_reviews.append(r)

            return cleaned_reviews
        except Exception as e:
            print(f"[Google Reviews] {e}")
            return []

    # ==========================================================
    # GOOGLE TRENDS
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=24)
    def fetch_google_trends(self, keywords: list) -> list:
        try:
            self.pytrend.build_payload(keywords, cat=0, timeframe="now 7-d", geo="UG")
            data = self.pytrend.interest_over_time()

            trends = []
            for keyword in keywords:
                if keyword not in data.columns:
                    continue
                trends.append({
                    "platform": "google_trends",
                    "topic": keyword,
                    "trend_score": int(data[keyword].iloc[-1])
                })
            return trends
        except Exception as e:
            print(f"[Google Trends] {e}")
            return []

    # ==========================================================
    # LOCAL NEWS
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=6)
    def fetch_local_news(self) -> list:
        feeds = [
            "https://www.monitor.co.ug/uganda/rss",
            "https://www.newvision.co.ug/category/news/feed"
        ]

        articles = []
        try:
            for url in feeds:
                feed = feedparser.parse(url)
                for entry in feed.entries[:20]:
                    articles.append({
                        "platform": "news",
                        "title": entry.get("title", ""),
                        "content": self._normalize_text(entry.get("summary", "")),
                        "source_url": entry.get("link", "")
                    })
            return articles
        except Exception as e:
            print(f"[News] {e}")
            return []

    # ==========================================================
    # WEATHER
    # ==========================================================

    @with_retry()
    @disk_cache(ttl_hours=3)
    def fetch_weather(self, city="Kampala") -> WeatherData:
        try:
            response = requests.get(
                "https://api.weatherapi.com/v1/current.json",
                params={
                    "key": os.getenv("WEATHER_API_KEY"),
                    "q": city
                },
                timeout=20
            )
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                platform="weather",
                city=city,
                temperature=float(data["current"]["temp_c"]),
                condition=data["current"]["condition"]["text"],
                humidity=float(data["current"]["humidity"])
            )
        except Exception as e:
            print(f"[Weather] {e}")
            return None

    # ==========================================================
    # MASTER COLLECTION METHOD
    # ==========================================================

    def collect_all_sources(self):
        x_data = []
        for q in get_twitter_queries():
            x_data.extend(self.fetch_x_data(query=q))

        tiktok_data = []
        for q in get_tiktok_queries():
            tiktok_data.extend(self.fetch_tiktok_data(query=q))

        insta_data = []
        for h in get_instagram_hashtags():
            insta_data.extend(self.fetch_instagram_hashtags(hashtag=h))

        reviews_data = []
        for target in get_google_reviews_targets():
            reviews_data.extend(self.fetch_google_reviews(search_term=target))

        trends_data = self.fetch_google_trends(get_google_trends_keywords())

        weather_data = []
        for city in get_weather_cities():
            w = self.fetch_weather(city=city)
            if w:
                weather_data.append(w)

        return {
            "x": [p.dict() for p in x_data],
            "tiktok": [p.dict() for p in tiktok_data],
            "instagram": [p.dict() for p in insta_data],
            "google_reviews": [r.dict() for r in reviews_data],
            "google_trends": trends_data,
            "news": self.fetch_local_news(),
            "weather": [w.dict() for w in weather_data]
        }