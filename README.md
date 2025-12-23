

---

# AI-QueryTube 🎥🔍

**Semantic Search Engine for YouTube Videos**

AI-QueryTube is an end-to-end **semantic search system for YouTube videos**.
The project extracts video metadata and transcripts, generates embeddings using transformer models, and allows users to search videos using **natural language queries** instead of exact keywords.

---

## 🚀 Project Overview

Traditional YouTube search relies heavily on keywords and metadata.
AI-QueryTube improves this by using **NLP and sentence embeddings** to understand the *meaning* of user queries and retrieve the most semantically relevant videos.

---

## 🧠 Key Features

* 📡 Extracts video metadata using **YouTube Data API**
* 📝 Fetches video transcripts using **YouTube Transcript API**
* 🧹 Cleans and normalizes text data
* 🔢 Generates embeddings using **Sentence Transformers**
* 📊 Performs EDA on metadata and transcripts
* 🔍 Semantic search using cosine similarity
* 🖥️ Interactive **Gradio-based search interface**
* 📁 Clean project structure with notebooks, scripts, and reports

---





## 🛠️ Technologies Used

* **Python**
* **YouTube Data API v3**
* **youtube-transcript-api**
* **Pandas / NumPy**
* **SentenceTransformers**
* **Scikit-learn**
* **Gradio**
* **Git & GitHub**

---

## 🔬 Workflow Summary

1. **Metadata Collection**

   * Fetch video ID, title, publish date using YouTube API

2. **Exploratory Data Analysis (EDA)**

   * Analyze publish frequency, title distribution, missing values

3. **Transcript Extraction**

   * Retrieve auto-generated or manual captions
   * Log videos without transcripts

4. **Text Cleaning**

   * Normalize transcripts and titles
   * Handle missing and noisy text

5. **Embedding Generation**

   * Encode transcripts and titles using transformer models

6. **Semantic Search**

   * Compare query embeddings with video embeddings
   * Rank results using cosine similarity

7. **UI Deployment**

   * Gradio app for interactive search experience

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set environment variables

```bash
export YOUTUBE_API_KEY=your_api_key_here
```

### 3️⃣ Run the pipeline

```bash
python scripts/run_pipeline.py
```

### 4️⃣ Launch the search app

```bash
python app/gradio_app.py
```

---

## 📌 Example Use Case

> **Query:** “videos explaining transformers in NLP”
> **Result:** Top 5 YouTube videos ranked by semantic relevance

---

## 📈 Future Improvements

* Add FAISS for faster similarity search
* Support multi-language transcripts
* Deploy as a web app
* Add user feedback-based ranking

---

## 👤 Author

**Aditya Sharma**
Computer Science Engineering Student
Intern – AI / NLP

---


