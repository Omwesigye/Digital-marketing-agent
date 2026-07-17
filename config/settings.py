import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# BRAND CONFIGURATION
# ==========================================================
# Default brand/restaurant settings
BRAND_NAME = os.getenv("BRAND_NAME", "Pizza Hut Kampala")
BRAND_KEYWORDS = os.getenv("BRAND_KEYWORDS", "pizza, delivery, food kampala").split(",")
BRAND_KEYWORDS = [k.strip() for k in BRAND_KEYWORDS if k.strip()]

# Competitor list
COMPETITORS = os.getenv("COMPETITORS", "").split(",")
COMPETITORS = [c.strip() for c in COMPETITORS if c.strip()]

# Locations and Markets
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Kampala")
DEFAULT_COUNTRY_CODE = os.getenv("DEFAULT_COUNTRY_CODE", "UG")

# ==========================================================
# DATABASE & APIS
# ==========================================================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# ==========================================================
# PIPELINE CONFIGURATION
# ==========================================================
# Real-time / schedule options
POLLING_INTERVAL_SECONDS = int(os.getenv("POLLING_INTERVAL_SECONDS", "300"))  # Default 5 minutes
CSV_RAW_DIR = os.path.join("data", "raw")
CSV_PROCESSED_DIR = os.path.join("data", "processed")

# Make sure data directories exist
os.makedirs(CSV_RAW_DIR, exist_ok=True)
os.makedirs(CSV_PROCESSED_DIR, exist_ok=True)
