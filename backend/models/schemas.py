from pydantic import BaseModel
from typing import Optional, List

class VideoInfo(BaseModel):
    title: str
    description: str
    thumbnail: str
    channel: str
    duration: int
    url: str

class TranscriptSegment(BaseModel):
    text: str
    start: float
    duration: float

class TranscriptResponse(BaseModel):
    video_info: VideoInfo
    transcript: List[TranscriptSegment]
    full_text: str

class BlogGenerationRequest(BaseModel):
    transcript: str
    prompt: str
    video_info: Optional[VideoInfo] = None

class BlogResponse(BaseModel):
    title: str
    content: str # Markdown/HTML
    summary: str

class FactCheckRequest(BaseModel):
    content: str

class FactCheckResponse(BaseModel):
    analysis: str

class WordPressPublishRequest(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    tags: Optional[List[str]] = []

class WordPressResponse(BaseModel):
    url: str
    post_id: int

class WhatsAppRequest(BaseModel):
    message: str
    url: Optional[str] = None

class PodcastRequest(BaseModel):
    text: str
    title: str
    description: str

class PodcastResponse(BaseModel):
    mp3_path: str
    status: str
    episode_url: Optional[str] = None
