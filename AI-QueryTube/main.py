import os   # os module ,used to read enviro varibles,used to get youtube api key

#responsible to run fastapi applica'n,get http request from browser
import uvicorn

#this library used to store and manipulate video data,makes sorting and filtering easy
import pandas as pd

#used for nmberical operations
import numpy as np

#fastapi-backend web app,
#query handles parametrs from url
#exception -uesd to proper api errors
from fastapi import FastAPI, Query, HTTPException

#allows frontend to comm with backend
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles  #used to serve frontend filesand to allow fastapi to load
from googleapiclient.discovery import build #used to connect to youtube data apiv3 and allow searching
from youtube_transcript_api import YouTubeTranscriptApi #fetch video transcripts from youtube ,used for sematic analysis instead of titles
from sentence_transformers import SentenceTransformer      #load pretarin nlp model,converts text into numerical
from sklearn.metrics.pairwise import cosine_similarity      # measure how similar 
 
app = FastAPI()     #create fastapi app instance ,used to define routes an apis
 
app.add_middleware(      # allow request from any browser
    CORSMiddleware,      #prevents errors
    allow_origins=["*"],    #allow all origins,get&post methods,headers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
try:             #loads model 
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")#lightweight,fasst,high accurate
    print("Model loaded successfully.")

    #catches error if model fails
except Exception as e:
    print(f"Error loading model: {e}")
    raise e
 


 #read apikey ,if not found uses fallback key,required to access utube dataapi
API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyAUueJtpbgNovyq-7oQsFWJ64zWJPc2z2w")
 
def get_youtube_service(): #helper function & create utube api sevice obj
    if API_KEY == "YOUR_YOUTUBE_API_KEY":
        raise HTTPException(
            status_code=500,
            detail="YouTube API Key is missing. Please set YOUTUBE_API_KEY environment variable or update the code."
        )
    return build("youtube", "v3", developerKey=API_KEY)
 
def get_videos(search_query, max_results=10):  #search utube videos based on query
    try:
        youtube = get_youtube_service()   #call utube search api 
        response = youtube.search().list(
            q=search_query,
            part="id,snippet", #fields
            type="video",        #filters only videos
            maxResults=max_results
        ).execute()
 
        videos = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            videos.append({      #extract useful data  and stores results in structed form
                "video_id": video_id,
                "title": snippet["title"],
                "description": snippet["description"],
                "thumbnail": snippet["thumbnails"]["high"]["url"]
                if "high" in snippet["thumbnails"]
                else snippet["thumbnails"]["default"]["url"]
            })
        return videos
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []
 
def get_transcripts(videos):   #retrieves subtitle for each video
    updated_videos = []
    for video in videos:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video["video_id"]) #fetch trabscript text
            transcript_text = " ".join([t["text"] for t in transcript_list])
            video["transcript"] = transcript_text #add transcript to video dict
        except Exception:        #handlevideo without subtitles
            video["transcript"] = ""
        updated_videos.append(video)
    return updated_videos
 
@app.get("/search")   #define getapi endpt  and called by frontend js

#accept query string fron url
def semantic_search(query: str = Query(..., description="The search query")):
    videos = get_videos(query, max_results=10)  #fetch utube videos
 
    if not videos:
        return {"results": []}
 
    videos_with_transcripts = get_transcripts(videos)
    df = pd.DataFrame(videos_with_transcripts)   #converts video data into dataframe
 
    df["combined_text"] = df["title"] + " " + df["transcript"]  #combine title + transcript for better meaning
    df["combined_text"].fillna("", inplace=True)
 
    embeddings = model.encode(df["combined_text"].tolist()) #convert text into numerical vectors
    query_embedding = model.encode(query)
 
    similarity_scores = cosine_similarity(
        query_embedding.reshape(1, -1),    #calculate similarity blw query and each video
        embeddings
    )[0]
 
    df["score"] = similarity_scores  #rank videos by semantic 
    results_df = df.sort_values(by="score", ascending=False)
 
    api_results = results_df[
        ["title", "description", "thumbnail", "video_id", "score"]
    ].to_dict(orient="records")
 
    return {"results": api_results}  #send ranked results to frontend
 
app.mount("/", StaticFiles(directory=".", html=True), name="static")   #serves frontend files & loads html file automatic
 
if __name__ == "__main__":    #start apiserver and runs on localhost 
    uvicorn.run(app, host="127.0.0.1", port=8000)   #allow browser access