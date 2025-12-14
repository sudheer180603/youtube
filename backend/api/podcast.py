from fastapi import HTTPException
from backend.models.schemas import PodcastResponse
from backend.utils.tts import text_to_speech
from backend.utils.spotify_uploader import upload_to_spotify
import logging

logger = logging.getLogger("YoutubeBlogApp")

async def create_podcast(text: str, title: str, description: str) -> PodcastResponse:
    try:
        # 1. Generate MP3
        logger.info("Generating MP3...")
        # Use first 3000 chars for TTS to avoid huge files/long processing in demo
        tts_text = text[:3000] 
        mp3_path = text_to_speech(tts_text, filename=f"{title[:20].replace(' ', '_')}.mp3")
        
        # 2. Upload to Spotify
        logger.info(f"Uploading {mp3_path} to Spotify...")
        # We'll run this synchronously or background? async/def mixing in FastAPI needs care.
        # Running Selenium in a separate thread/process is better, but for simplicity here we block.
        status = upload_to_spotify(mp3_path, title, description)
        
        return PodcastResponse(
            mp3_path=mp3_path,
            status=f"MP3 Generated. Upload Status: {status}"
        )
    except Exception as e:
        logger.error(f"Podcast creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
