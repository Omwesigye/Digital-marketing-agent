# AI Restaurant Marketing Platform (AgentScope)

This platform scrapes, analyzes, tracks competitors, drafts content (with human approval), and executes marketing campaign workflows for restaurant brands using the **AgentScope** multi-agent framework.

## Key Features

1. **Multi-Source Scraping**: Scrapes X (Twitter), TikTok, Instagram, Google Reviews, Google Trends, local news feeds, and weather via Apify and local APIs.
2. **Sentiment Analysis**: Quick VADER parsing combined with deep LLM sentiment, emotion, and customer needs classification.
3. **Competitor Intelligence**: Aggregates ratings, strengths, and weaknesses from competitor Google Maps reviews.
4. **Insights Synthesis**: Aggregates all social signals and trends to suggest operations and marketing opportunities.
5. **Draft & Approval Flow**: Content drafts are created in the database and must be approved before publishing.
6. **Retention Emails**: Dynamically targets churned/regular customers using personalized Resend email campaigns.

---

## Installation

```bash
pip install -r requirements.txt
```

Ensure you have a `.env` file containing:
```ini
APIFY_TOKEN=your_apify_token
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# LLM Providers (Configure at least one)
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Email
RESEND_API_KEY=your_resend_api_key
```

---

## Execution Modes

Run the full pipeline (Scrape → Analyze → Content Drafts):
```bash
python main.py --mode full --model-config gemini_config
```

Run only the scraper/listening pipeline:
```bash
python main.py --mode listen
```

Run real-time continuous listening loop:
```bash
python main.py --mode realtime --interval 300
```

Execute an email retention campaign:
```bash
python main.py --mode campaign --campaign-name "Weekend Pizza Offer" --campaign-goal "Promote new pizza and give 20% off delivery"
```

Publish approved content drafts:
```bash
python main.py --mode publish
```
