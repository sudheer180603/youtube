from twilio.rest import Client
from backend.config.settings import settings
import logging

logger = logging.getLogger("YoutubeBlogApp")

def send_whatsapp_message(body: str) -> str:
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        logger.warning("Twilio credentials missing")
        return "Twilio not configured"
        
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            body=body,
            to=settings.TWILIO_WHATSAPP_TO
        )
        
        return message.sid
    except Exception as e:
        logger.error(f"Twilio error: {e}")
        raise
