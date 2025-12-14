from typing import List, Dict, Any
import logging
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from backend.models.schemas import VideoInfo, TranscriptSegment, TranscriptResponse

logger = logging.getLogger("YoutubeBlogApp")

def get_video_info(url: str) -> VideoInfo:
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # If it's a playlist, info['entries'] will exist, but we might just take the first one or handle differently
            # For this MVP, let's assume single video processing or extraction of the specific video from URL
            # If URL is a playlist, yt-dlp returns type='playlist'.
            
            if info.get('_type') == 'playlist':
                 # Just get info of the first video for now to return valid VideoInfo
                 # The user might want the whole playlist processed, but the UI flow "Fetch Transcript" suggests a single context initially or merged.
                 # Let's verify if 'entries' is populated
                 if 'entries' in info:
                     first_entry = list(info['entries'])[0]
                     # Some fields might be missing in flat extraction, needing a re-extract
                     return get_video_info(first_entry['url'])
            
            return VideoInfo(
                title=info.get('title', 'Unknown Title'),
                description=info.get('description', ''),
                thumbnail=info.get('thumbnail', ''),
                channel=info.get('uploader', 'Unknown Channel'),
                duration=info.get('duration', 0),
                url=info.get('webpage_url', url)
            )
        except Exception as e:
            logger.error(f"Error fetching video info: {e}")
            raise

def get_video_id(url: str) -> str:
    # yt-dlp is robust at extracting ID from various URL formats
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('id')

def get_transcript(video_id: str) -> List[TranscriptSegment]:
    try:
        # Try finding manually created transcripts first, then generated
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Priority: English manual -> English auto -> Any manual -> Any auto
        try:
             transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                # Get the first available
                transcript = next(iter(transcript_list))
        
        data = transcript.fetch()
        return [
            TranscriptSegment(
                text=item['text'],
                start=item['start'],
                duration=item['duration']
            ) for item in data
        ]
            
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        logger.warning(f"No transcript found for {video_id}: {e}")
        return []
    except Exception as e:
        logger.error(f"Error extracting transcript: {e}")
        raise

async def process_youtube_url(url: str) -> TranscriptResponse:
    try:
        video_info = get_video_info(url)
        video_id = get_video_id(url)
        
        segments = get_transcript(video_id)
        full_text = " ".join([seg.text for seg in segments])
        
        return TranscriptResponse(
            video_info=video_info,
            transcript=segments,
            full_text=full_text
        )
    except Exception as e:
        logger.error(f"Failed to process YouTube URL: {e}")
        raise
