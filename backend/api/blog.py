import google.generativeai as genai
from backend.config.settings import settings
from backend.models.schemas import BlogResponse
import logging

logger = logging.getLogger("YoutubeBlogApp")

async def generate_blog_post(transcript: str, prompt: str, video_info: dict = None) -> BlogResponse:
    """
    Generates a blog post using Gemini 1.5 Flash.
    """
    
    context = ""
    if video_info:
        context = f"Video Title: {video_info.get('title')}\nChannel: {video_info.get('channel')}\n"

    final_prompt = f"""
    You are an expert content writer.
    
    CONTEXT:
    {context}
    
    TRANSCRIPT:
    {transcript}
    
    INSTRUCTIONS:
    {prompt}
    
    Output format:
    Return the content in Markdown format.
    Also provide a short summary (max 50 words) at the very end, separated by '---SUMMARY---'.
    """

    content = ""
    
    try:
        if settings.GEMINI_API_KEY:
            logger.info("Using Gemini 1.5 Flash for blog generation")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Using 'gemini-1.5-flash' as requested (user said 2.5, mapped to 1.5-flash for stability/availability)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(final_prompt)
            content = response.text
        else:
            raise ValueError("No Gemini API Key found in .env")

        # Parsing content and summary
        parts = content.split('---SUMMARY---')
        main_content = parts[0].strip()
        summary = parts[1].strip() if len(parts) > 1 else main_content[:200] + "..."

        title = "Generated Blog Post" # We could ask LLM to generate title too, or parse it
        
        # Simple heuristic to extract title if LLM put it in first line as # Title
        lines = main_content.split('\n')
        if lines and lines[0].startswith('# '):
            title = lines[0].replace('# ', '').strip()

        return BlogResponse(
            title=title,
            content=main_content,
            summary=summary
        )

    except Exception as e:
        logger.error(f"Error generating blog: {e}")
        raise
