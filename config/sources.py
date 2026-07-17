from config.settings import BRAND_NAME, COMPETITORS, DEFAULT_CITY

# Generate dynamic search terms based on configured restaurant and competitors
def get_twitter_queries():
    queries = [
        f"{DEFAULT_CITY} food",
        f"{DEFAULT_CITY} restaurant",
        BRAND_NAME.lower(),
    ]
    for comp in COMPETITORS:
        queries.append(comp.lower())
    return queries

def get_tiktok_queries():
    return [
        f"{DEFAULT_CITY} food",
        f"{DEFAULT_CITY} eats",
        BRAND_NAME.lower(),
    ]

def get_instagram_hashtags():
    # Strip spaces and make lower
    brand_tag = BRAND_NAME.replace(" ", "").lower()
    city_food_tag = f"{DEFAULT_CITY.lower()}food"
    return [brand_tag, city_food_tag, "foodie", "restaurant"]

def get_google_reviews_targets():
    targets = [BRAND_NAME]
    for comp in COMPETITORS:
        targets.append(comp)
    return targets

def get_google_trends_keywords():
    return [
        "pizza",
        "burger",
        "fast food",
        "restaurant",
        "delivery"
    ]

def get_news_feeds():
    return [
        "https://www.monitor.co.ug/uganda/rss",
        "https://www.newvision.co.ug/category/news/feed"
    ]

def get_weather_cities():
    return [DEFAULT_CITY]
