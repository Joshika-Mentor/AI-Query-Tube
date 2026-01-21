# 🔍 AI Query Tube  
### Semantic YouTube Video Search using Transcripts

AI Query Tube is a full-stack web application that enables **semantic search over YouTube videos** by analyzing **video transcripts** instead of relying only on titles or keywords. 

---

## 🧠 Problem Statement
Traditional YouTube search relies heavily on keywords and metadata, which often fails to capture the **true meaning** of user intent.

AI Query Tube solves this by:
- Extracting video transcripts
- Converting them into semantic embeddings
- Ranking videos by **meaning similarity**

---

## ✨ Key Features
- 🔍 Semantic (meaning-based) search
- 📄 Transcript-driven relevance
- ⚡ Parallel transcript processing
- 🧠 NLP embeddings using MPNet
- 📊 Cosine similarity ranking
- 🎥 In-app YouTube video playback
- 🧾 Transcript preview toggle
- 🚀 Cached responses for fast repeat searches

---

## 🏗️ Tech Stack

### Frontend
- React.js
- JavaScript (ES6)
- HTML5, CSS
- Fetch API
- YouTube Embed (iframe)

### Backend
- FastAPI
- Python
- YouTube Data API v3
- yt-dlp (subtitle extraction)
- Sentence Transformers
- `all-mpnet-base-v2`
- scikit-learn
- ThreadPoolExecutor
- dotenv
- Uvicorn

---

## 🧩 Architecture Overview
User
↓
React Frontend
↓
FastAPI Backend
↓
YouTube API + Transcript Engine
↓
Embedding & Similarity Ranking
↓
Ranked Results


---

## ⚙️ Backend Workflow
1. Receive user query
2. Check cache
3. Fetch YouTube videos
4. Extract transcripts in parallel
5. Generate embeddings
6. Compute cosine similarity
7. Rank videos
8. Cache and return results

---

## 📈 Performance Optimizations
| Optimization | Impact |
|---|---|
| Parallel transcript fetching | ~70% faster |
| In-memory caching | Instant repeat searches |
| CPU-based thread tuning | Safe scaling |
| Loading skeleton UI | Better UX |

---

## 🛠️ Local Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

