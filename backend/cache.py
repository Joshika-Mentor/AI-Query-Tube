# cache.py

from typing import Dict, List

# Cache search results by query
query_cache: Dict[str, List[dict]] = {}

# Cache transcripts by video_id
transcript_cache: Dict[str, str] = {}

def get_cached(query: str):
    return query_cache.get(query)

def set_cache(query: str, results):
    query_cache[query] = results

def get_transcript_cached(video_id: str):
    return transcript_cache.get(video_id)

def set_transcript_cached(video_id: str, transcript: str):
    transcript_cache[video_id] = transcript
