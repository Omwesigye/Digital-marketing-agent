from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime

class RawSignal(BaseModel):
    id: Optional[str] = None
    platform: str
    content: Optional[str] = None
    author: Optional[str] = "anonymous"
    source_url: Optional[str] = None
    engagement: Optional[int] = 0
    raw_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    scraped_at: Optional[datetime] = None

class SentimentResult(BaseModel):
    id: Optional[str] = None
    signal_id: str
    sentiment_label: str  # positive, negative, neutral
    sentiment_score: float  # -1.0 to 1.0
    emotions: Optional[Dict[str, float]] = Field(default_factory=dict)
    key_phrases: Optional[List[str]] = Field(default_factory=list)
    customer_needs: Optional[List[str]] = Field(default_factory=list)
    is_urgent: Optional[bool] = False
    analyzed_at: Optional[datetime] = None

class CompetitorInsight(BaseModel):
    id: Optional[str] = None
    competitor_name: str
    platform: Optional[str] = None
    metric_type: str  # rating, review_count, sentiment
    metric_value: float
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tracked_at: Optional[datetime] = None

class Insight(BaseModel):
    id: Optional[str] = None
    insight_type: str  # trend, opportunity, threat, recommendation
    title: str
    description: Optional[str] = None
    confidence: Optional[float] = 1.0
    data_sources: Optional[List[str]] = Field(default_factory=list)  # list of raw_signal IDs
    action_items: Optional[List[str]] = Field(default_factory=list)
    created_at: Optional[datetime] = None

class ContentPiece(BaseModel):
    id: Optional[str] = None
    content_type: str  # social_post, email
    platform: str  # twitter, instagram, tiktok, email
    title: Optional[str] = None
    body: str
    hashtags: Optional[List[str]] = Field(default_factory=list)
    media_suggestions: Optional[List[str]] = Field(default_factory=list)
    status: Optional[str] = "draft"  # draft, approved, published, rejected
    insight_id: Optional[str] = None
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

class Campaign(BaseModel):
    id: Optional[str] = None
    name: str
    goal: Optional[str] = None
    target_audience: Optional[str] = None
    channels: Optional[List[str]] = Field(default_factory=list)
    status: Optional[str] = "planning"  # planning, active, paused, completed
    content_ids: Optional[List[str]] = Field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: Optional[Dict[str, Any]] = Field(default_factory=dict)
    created_at: Optional[datetime] = None

class EmailContact(BaseModel):
    id: Optional[str] = None
    email: str  # using simple string to avoid strict email validation issues if testing
    name: Optional[str] = None
    segment: Optional[str] = "regular"  # vip, regular, churning, new
    engagement_score: Optional[float] = 0.0
    last_opened: Optional[datetime] = None
    last_clicked: Optional[datetime] = None
    subscribed_at: Optional[datetime] = None
    unsubscribed: Optional[bool] = False

class EmailSend(BaseModel):
    id: Optional[str] = None
    campaign_id: Optional[str] = None
    contact_id: str
    subject: str
    body: str
    status: Optional[str] = "sent"  # sent, opened, clicked, bounced
    sent_at: Optional[datetime] = None
