from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import os
import traceback

load_dotenv()

from youtube_search import search_youtube
from transcripts import get_transcript
from embeddings import rank_videos
from cache import get_cached, set_cache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def optimal_thread_count():
    cpu = os.cpu_count() or 4
    return min(8, cpu * 2)  # IO-bound safe limit

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/search")
def search(query: str):
    try:
        # 1️⃣ Query cache
        cached = get_cached(query)
        if cached:
            return {
                "status": "completed",
                "results": cached
            }

        # 2️⃣ YouTube search
        videos = search_youtube(query, max_results=8)
        if not videos:
            return {
                "status": "no_results",
                "results": []
            }

        # 3️⃣ Parallel transcript fetching
        thread_count = optimal_thread_count()
        print(f"🔄 Fetching transcripts using {thread_count} threads")

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            transcripts = list(
                executor.map(
                    lambda v: get_transcript(v["video_id"]),
                    videos
                )
            )

        # 4️⃣ Attach transcripts (fallback to title)
        enriched = []
        for v, t in zip(videos, transcripts):
            v["transcript"] = t if t else v["title"]
            enriched.append(v)

        # 5️⃣ Rank videos semantically
        print("🧠 Ranking videos")
        ranked = rank_videos(query, enriched)

        # 6️⃣ Cache results
        set_cache(query, ranked)

        return {
            "status": "completed",
            "results": ranked
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }
