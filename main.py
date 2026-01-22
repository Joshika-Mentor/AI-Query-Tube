
# Import FastAPI framework to build backend APIs
from fastapi import FastAPI, Query

# Import CORS middleware to allow frontend to talk to backend
from fastapi.middleware.cors import CORSMiddleware

# Used to connect and communicate with YouTube Data API
from googleapiclient.discovery import build

# Used to fetch subtitles (transcripts) from YouTube videos
from youtube_transcript_api import YouTubeTranscriptApi

# Used for semantic understanding of text
from sentence_transformers import SentenceTransformer

# Used to calculate similarity between query and video text
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- CONFIGURATION ----------------

# YouTube API key (used to access YouTube data)
YOUTUBE_API_KEY = "AIzaSyDuxU60mIcNHnQdYwtugdAexWzn37TahUM"

# Number of videos we want to fetch and return
MAX_RESULTS = 5


# APPLICATION SETUP 

# Create a FastAPI application instance
app = FastAPI()

# Enable CORS so frontend (browser) can call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow requests from any origin
    allow_methods=["*"],      # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],      # Allow all headers
)

# Create YouTube API service object using API key
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Load a pre-trained AI model for semantic understanding
model = SentenceTransformer("all-MiniLM-L6-v2")


#  HELPER FUNCTIONS 

# This function searches YouTube based on user query
def get_youtube_videos(query):

    # Call YouTube search API
    response = youtube.search().list(
        part="snippet",        # Request basic video details
        q=query,               # Search keyword entered by user
        type="video",          # Only search for videos
        maxResults=MAX_RESULTS # Limit number of results
    ).execute()                # Execute the API request

    # Empty list to store video details
    videos = []

    # Loop through each video returned by YouTube
    for item in response["items"]:

        # Store required details in dictionary format
        videos.append({
            "video_id": item["id"]["videoId"],  # Unique video ID
            "title": item["snippet"]["title"],  # Video title
            "channel": item["snippet"]["channelTitle"],  # Channel name
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"], # Thumbnail
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}" # Video URL
        })

    # Return list of videos
    return videos


# This function tries to fetch transcript for a given video
def get_transcript(video_id):
    try:
        # Request transcript using video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all subtitle lines into one string
        return " ".join([t["text"] for t in transcript])

    except:
        # If transcript is not available, return empty string
        return ""


# This function ranks videos based on semantic similarity
def semantic_rank(query, videos):

    # List to store combined text (title + transcript)
    texts = []

    # List to store corresponding videos
    valid_videos = []

    # Loop through each video
    for v in videos:

        # Get transcript for the video
        transcript = get_transcript(v["video_id"])

        # Combine title and transcript for better meaning
        combined_text = v["title"] + " " + transcript

        # Store combined text
        texts.append(combined_text)

        # Store video details
        valid_videos.append(v)

    # Convert user query into embedding (numeric form)
    query_embedding = model.encode([query])

    # Convert all video texts into embeddings
    doc_embeddings = model.encode(texts)

    # Calculate similarity between query and each video text
    scores = cosine_similarity(query_embedding, doc_embeddings)[0]

    # Sort videos based on similarity score (highest first)
    ranked = sorted(
        zip(valid_videos, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Return videos in ranked order (ignore score in output)
    return [v for v, _ in ranked]


# API ENDPOINT 

# This API is called when frontend sends request to /search
@app.get("/search")
def search_videos(query: str = Query(...)):

    # Step 1: Fetch videos from YouTube based on query
    videos = get_youtube_videos(query)

    # Step 2: Rank videos using semantic similarity
    ranked_videos = semantic_rank(query, videos)

    # Step 3: Return top N videos to frontend
    return ranked_videos[:MAX_RESULTS]