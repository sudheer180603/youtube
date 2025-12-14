import os
from gtts import gTTS
from backend.config.settings import settings
import logging
import uuid

logger = logging.getLogger("YoutubeBlogApp")

def text_to_speech(text: str, filename: str = None) -> str:
    """
    Converts text to MP3 using gTTS.
    Returns the absolute path to the saved file.
    """
    try:
        # Generate a unique filename if not provided
        if not filename:
            filename = f"podcast_{uuid.uuid4().hex[:8]}.mp3"
        
        # Ensure filename ends with .mp3
        if not filename.endswith(".mp3"):
            filename += ".mp3"
            
        file_path = os.path.join(settings.PODCAST_DIR, filename)
        
        # gTTS processing
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(file_path)
        
        return os.path.abspath(file_path)
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        raise
