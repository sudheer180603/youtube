import requests
import base64
from backend.config.settings import settings
from backend.models.schemas import WordPressResponse
import logging

logger = logging.getLogger("YoutubeBlogApp")

def publish_post(title: str, content: str, excerpt: str = None, tags: list = []) -> WordPressResponse:
    if not settings.WORDPRESS_URL or not settings.WORDPRESS_USERNAME or not settings.WORDPRESS_APP_PASSWORD:
        raise ValueError("WordPress credentials missing in .env")

    url = f"{settings.WORDPRESS_URL.rstrip('/')}/wp-json/wp/v2/posts"
    
    credentials = f"{settings.WORDPRESS_USERNAME}:{settings.WORDPRESS_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': title,
        'content': content,
        'status': 'publish', # or 'draft'
        'excerpt': excerpt if excerpt else '',
        # 'tags': tags # Requires tag IDs, skipping for MVP complexity
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        post_data = response.json()
        return WordPressResponse(
            url=post_data.get('link'),
            post_id=post_data.get('id')
        )
    except Exception as e:
        logger.error(f"WordPress publish error: {e}")
        raise
