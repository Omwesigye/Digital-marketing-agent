-- Raw scraped restaurant data signals
CREATE TABLE IF NOT EXISTS raw_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform TEXT NOT NULL,           -- x, tiktok, instagram, news, weather, google_reviews, google_trends
    content TEXT,
    author TEXT DEFAULT 'anonymous',
    source_url TEXT,
    engagement INTEGER DEFAULT 0,
    raw_metadata JSONB DEFAULT '{}'::jsonb,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sentiment analysis results
CREATE TABLE IF NOT EXISTS sentiment_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    signal_id UUID REFERENCES raw_signals(id) ON DELETE CASCADE,
    sentiment_label TEXT NOT NULL,             -- positive, negative, neutral
    sentiment_score FLOAT NOT NULL,            -- -1.0 to 1.0
    emotions JSONB DEFAULT '{}'::jsonb,        -- e.g., {"joy": 0.8, "anger": 0.1}
    key_phrases TEXT[] DEFAULT '{}',
    customer_needs TEXT[] DEFAULT '{}',
    is_urgent BOOLEAN DEFAULT FALSE,
    analyzed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Competitor intelligence benchmarks
CREATE TABLE IF NOT EXISTS competitor_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competitor_name TEXT NOT NULL,
    platform TEXT,
    metric_type TEXT,                          -- rating, review_count, sentiment
    metric_value FLOAT,
    details JSONB DEFAULT '{}'::jsonb,
    tracked_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated restaurant insights & recommendations
CREATE TABLE IF NOT EXISTS insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    insight_type TEXT NOT NULL,                -- trend, opportunity, threat, recommendation
    title TEXT NOT NULL,
    description TEXT,
    confidence FLOAT DEFAULT 1.0,
    data_sources JSONB DEFAULT '[]'::jsonb,    -- list of raw_signal IDs
    action_items TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated marketing content drafts (with human-approval workflow)
CREATE TABLE IF NOT EXISTS content_library (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_type TEXT NOT NULL,                -- social_post, email
    platform TEXT NOT NULL,                    -- twitter, instagram, tiktok, email
    title TEXT,
    body TEXT NOT NULL,
    hashtags TEXT[] DEFAULT '{}',
    media_suggestions JSONB DEFAULT '[]'::jsonb,
    status TEXT DEFAULT 'draft',               -- draft, approved, published, rejected
    insight_id UUID REFERENCES insights(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ
);

-- Marketing campaign tracking
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    goal TEXT,
    target_audience TEXT,
    channels TEXT[] DEFAULT '{}',              -- ['email', 'twitter', 'instagram']
    status TEXT DEFAULT 'planning',            -- planning, active, paused, completed
    content_ids UUID[] DEFAULT '{}',
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    metrics JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Email contacts for loyalty & retention
CREATE TABLE IF NOT EXISTS email_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    segment TEXT DEFAULT 'regular',            -- vip, regular, churning, new
    engagement_score FLOAT DEFAULT 0,
    last_opened TIMESTAMPTZ,
    last_clicked TIMESTAMPTZ,
    subscribed_at TIMESTAMPTZ DEFAULT NOW(),
    unsubscribed BOOLEAN DEFAULT FALSE
);

-- Email campaign send history
CREATE TABLE IF NOT EXISTS email_sends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL,
    contact_id UUID REFERENCES email_contacts(id) ON DELETE CASCADE,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT DEFAULT 'sent',                -- sent, opened, clicked, bounced
    sent_at TIMESTAMPTZ DEFAULT NOW()
);
