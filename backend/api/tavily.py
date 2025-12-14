from tavily import TavilyClient
from backend.config.settings import settings
from backend.models.schemas import FactCheckResponse
import logging

logger = logging.getLogger("YoutubeBlogApp")

async def check_facts(content: str) -> FactCheckResponse:
    if not settings.TAVILY_API_KEY:
        logger.warning("No Tavily API Key found")
        return FactCheckResponse(analysis="Fact checking disabled (No API Key).")
    
    try:
        tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)
        
        # We can optimize this by extracting key claims first using LLM, but for simplicity:
        # We will search for the first few sentences or a summary query
        
        # Simplified approach: Search for the blog topic/title logic would be better
        # But here we just take the first 400 chars as query context roughly
        query = content[:400].replace('\n', ' ')
        
        response = tavily.search(query=query, search_depth="advanced")
        results = response.get('results', [])
        
        summary = f"Found {len(results)} relevant sources.\n"
        for res in results[:3]:
            summary += f"- [{res['title']}]({res['url']})\n"
            
        # ideally we would use an LLM to compare 'content' vs 'results'
        # For this MVP, we return the sources found.
        
        return FactCheckResponse(analysis=summary)

    except Exception as e:
        logger.error(f"Tavily error: {e}")
        return FactCheckResponse(analysis=f"Error checking facts: {str(e)}")
