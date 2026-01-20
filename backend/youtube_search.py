import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

if not API_KEY:
    raise RuntimeError("❌ YOUTUBE_API_KEY is not set in environment variables")

def search_youtube(query: str, max_results: int = 8):
    params = {
        "part": "snippet",
        "q": query,
        "key": API_KEY,
        "type": "video",
        "maxResults": max_results
    }

    res = requests.get(SEARCH_URL, params=params).json()

    if "items" not in res:
        print("YouTube API error:", res)
        return []

    videos = []
    for item in res["items"]:
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "published_date": item["snippet"]["publishedAt"]
        })

    return videos
