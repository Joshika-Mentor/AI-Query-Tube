# fastapi_youtube_recommend.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Initialize FastAPI
app = FastAPI()

# CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your YouTube Data API key
YOUTUBE_API_KEY = "AIzaSyBMRwTJ24ZEmG5jdyeKfBcz2egZEGQw2B8"
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Sentence transformer for semantic ranking
model = SentenceTransformer('all-MiniLM-L6-v2')


def fetch_youtube_videos(query, max_results=20):
    """
    Fetch YouTube videos based on query.
    Filters out shorts and prefers long videos.
    """
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="relevance",
        videoDuration="long"  # Prefer course-like long videos
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        channel_title = item["snippet"]["channelTitle"]

        # Fetch video stats
        stats_request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        stats_response = stats_request.execute()
        stats = stats_response["items"][0]["statistics"]
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))

        videos.append({
            "video_id": video_id,
            "title": title,
            "description": description,
            "thumbnail": thumbnail,
            "channel": channel_title,
            "views": views,
            "likes": likes
        })
    return videos


def rank_videos(videos, query):
    """
    Rank videos based on:
    1. Views
    2. Likes
    3. Semantic similarity to query
    """
    if len(videos) == 0:
        return []

    # Semantic similarity
    video_texts = [v["title"] + " " + v["description"] for v in videos]
    video_embs = model.encode(video_texts)
    query_emb = model.encode([query])
    similarity_scores = cosine_similarity(query_emb, video_embs)[0]

    # Normalize views and likes
    max_views = max([v["views"] for v in videos]) or 1
    max_likes = max([v["likes"] for v in videos]) or 1

    for i, v in enumerate(videos):
        score = 0.5 * (v["views"]/max_views) + 0.3 * (v["likes"]/max_likes) + 0.2 * similarity_scores[i]
        v["score"] = float(score)  # <-- convert numpy.float32 to Python float

    # Sort videos by final score
    videos_sorted = sorted(videos, key=lambda x: x["score"], reverse=True)
    return videos_sorted



@app.get("/search")
def search_videos(query: str = Query(..., min_length=1)):
    """
    Endpoint to search YouTube videos with ranking
    """
    videos = fetch_youtube_videos(query)
    ranked_videos = rank_videos(videos, query)
    return {"results": ranked_videos}
main.py