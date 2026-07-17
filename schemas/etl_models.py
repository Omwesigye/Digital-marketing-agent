from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Any
from datetime import datetime

class Profile(BaseModel):
    platform: str
    username: str
    bio: Optional[str] = None
    follower_count: Optional[int] = 0
    following_count: Optional[int] = 0
    profile_picture_url: Optional[str] = None

class Comment(BaseModel):
    id: Optional[str] = None
    author: str
    text: str
    likes: Optional[int] = 0
    replies: Optional[int] = 0
    timestamp: Optional[datetime] = None

class Post(BaseModel):
    platform: str
    id: Optional[str] = None
    author: str
    caption: str
    timestamp: Optional[datetime] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    source_url: Optional[str] = None
    engagement_likes: Optional[int] = 0
    engagement_comments: Optional[int] = 0
    engagement_shares: Optional[int] = 0
    comments: List[Comment] = Field(default_factory=list)

class Hashtag(BaseModel):
    platform: str
    tag: str
    post_count: Optional[int] = 0
    top_content: List[Post] = Field(default_factory=list)

class SearchResult(BaseModel):
    platform: str
    keyword: str
    accounts: List[Profile] = Field(default_factory=list)
    posts: List[Post] = Field(default_factory=list)

class Review(BaseModel):
    platform: str = "google_reviews"
    author: str
    rating: float
    text: str
    timestamp: Optional[datetime] = None

class WeatherData(BaseModel):
    platform: str = "weather"
    city: str
    temperature: float
    condition: str
    humidity: float

class ExtractedData(BaseModel):
    profiles: List[Profile] = Field(default_factory=list)
    posts: List[Post] = Field(default_factory=list)
    hashtags: List[Hashtag] = Field(default_factory=list)
    search_results: List[SearchResult] = Field(default_factory=list)
    reviews: List[Review] = Field(default_factory=list)
    weather: List[WeatherData] = Field(default_factory=list)
    raw_other: List[Any] = Field(default_factory=list)
