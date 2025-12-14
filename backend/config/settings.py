import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    WORDPRESS_URL = os.getenv("WORDPRESS_URL")
    WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
    WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")
    
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
    TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")
    
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    SPOTIFY_EMAIL = os.getenv("SPOTIFY_EMAIL")
    SPOTIFY_PASSWORD = os.getenv("SPOTIFY_PASSWORD")
    
    # Path to save audio files
    PODCAST_DIR = "podcasts"
    if not os.path.exists(PODCAST_DIR):
        os.makedirs(PODCAST_DIR)

settings = Settings()
