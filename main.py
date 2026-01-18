from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

app = FastAPI(title="QueryTube Backend")

# ----------------------
# CORS: allow frontend
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# YOUTUBE API KEY
# ----------------------
API_KEY = "AIzaSyCOYxp0CywxmWTnnQmu7JZ3stYrcpbxH3A"
youtube = build("youtube", "v3", developerKey=API_KEY)

# ----------------------
# NLP Model
# ----------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------
# Get videos from YouTube
# ----------------------
def get_videos(search_query, max_results=5):
    response = youtube.search().list(
        q=search_query,
        part="id,snippet",
        type="video",
        maxResults=max_results
    ).execute()

    videos = []
    for item in response["items"]:
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"]
        })
    return videos


# ----------------------
# Get transcripts
# ----------------------
def get_transcripts(video_ids):
    transcripts = []
    for vid in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
            transcripts.append(" ".join([t["text"] for t in transcript]))
        except:
            transcripts.append("")
    return transcripts


# ----------------------
# SEARCH ENDPOINT
# ----------------------
@app.get("/search")
def semantic_search(query: str = Query(...), max_results: int = 5):
    """
    Frontend calls: /search?query=jenny
    Returns results = [{video_id, title, description, thumbnail, score, video_url}]
    """

    # 1️⃣ Fetch videos
    videos = get_videos(query, max_results)
    video_ids = [v["video_id"] for v in videos]
    titles = [v["title"] for v in videos]

    # 2️⃣ Fetch transcripts
    transcripts = get_transcripts(video_ids)

    # 3️⃣ Combine text and create embeddings
    combined_text = [t + " " + tr for t, tr in zip(titles, transcripts)]
    embeddings = model.encode(combined_text)
    query_embedding = model.encode([query])

    # 4️⃣ Compute similarity
    scores = cosine_similarity(query_embedding.reshape(1, -1), embeddings)[0]

    # 5️⃣ Build final results
    results = []
    for i in range(len(videos)):
        results.append({
            "video_id": videos[i]["video_id"],
            "title": videos[i]["title"],
            "description": transcripts[i][:200] or "No description available",
            "thumbnail": f"https://img.youtube.com/vi/{videos[i]['video_id']}/hqdefault.jpg",
            "score": float(scores[i]),
            "video_url": f"https://www.youtube.com/watch?v={videos[i]['video_id']}"
        })

    # 6️⃣ Sort by relevance
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"results": results}
