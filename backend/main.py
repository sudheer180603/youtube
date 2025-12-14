from fastapi import FastAPI, HTTPException
from backend.models.schemas import (
    TranscriptResponse, 
    BlogGenerationRequest, BlogResponse, 
    FactCheckRequest, FactCheckResponse,
    WordPressPublishRequest, WordPressResponse,
    WhatsAppRequest,
    PodcastRequest, PodcastResponse
)
from backend.api import youtube, blog, tavily, wordpress, whatsapp, podcast
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YoutubeBlogApp")

app = FastAPI(title="YouTube to Blog Automation API")

@app.get("/")
def read_root():
    return {"message": "Welcome to YouTube to Blog Automation API"}

@app.get("/transcript", response_model=TranscriptResponse)
async def get_transcript_endpoint(url: str):
    logger.info(f"Fetching transcript for: {url}")
    return await youtube.process_youtube_url(url)

@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog_endpoint(request: BlogGenerationRequest):
    logger.info("Generating blog post...")
    return await blog.generate_blog_post(request.transcript, request.prompt, request.video_info.dict() if request.video_info else None)

@app.post("/check-facts", response_model=FactCheckResponse)
async def check_facts_endpoint(request: FactCheckRequest):
    logger.info("Checking facts...")
    return await tavily.check_facts(request.content)

@app.post("/publish-wordpress", response_model=WordPressResponse)
def publish_wordpress_endpoint(request: WordPressPublishRequest):
    logger.info("Publishing to WordPress...")
    return wordpress.publish_post(request.title, request.content, request.excerpt, request.tags)

@app.post("/send-whatsapp")
def send_whatsapp_endpoint(request: WhatsAppRequest):
    logger.info("Sending WhatsApp message...")
    sid = whatsapp.send_whatsapp_message(request.message)
    return {"status": "sent", "sid": sid}

@app.post("/create-and-upload-podcast", response_model=PodcastResponse)
async def create_podcast_endpoint(request: PodcastRequest):
    logger.info("Creating podcast...")
    return await podcast.create_podcast(request.text, request.title, request.description)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
