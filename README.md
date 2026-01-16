📖 Project Overview

AI QueryTube is an AI-based semantic search system for YouTube videos.
Unlike traditional keyword search, this project allows users to search videos based on meaning using transformer-based embeddings.

The system extracts video data from a YouTube channel, converts video transcripts into embeddings, and retrieves the most relevant videos for a user query using cosine similarity.

🎯 Project Objectives

Extract video metadata from a YouTube channel using YouTube Data API

Convert video transcripts into text for AI processing

Generate semantic embeddings using a transformer model

Implement semantic search based on similarity scoring

Build an interactive UI for searching videos

🧠 Technologies Used

Python

YouTube Data API

youtube-transcript-api

SentenceTransformers (all-MiniLM-L6-v2)

NumPy

Scikit-learn

Gradio

🏗️ Project Architecture

Video Collection

Fetch video ID, title, and published date from a YouTube channel using the uploads playlist.

Transcript Extraction

Extract subtitles using YouTube Transcript API with fallback handling.

Text Processing

Combine video titles and transcripts for better semantic context.

Embedding Generation

Convert text into vector embeddings using a transformer model.

Semantic Search

Compare user query embeddings with video embeddings using cosine similarity.

User Interface

Provide a Gradio-based UI to perform semantic search interactively.

⚠️ Important Note

Not all YouTube videos expose transcripts via the API.
Videos without accessible transcripts are filtered out before embedding generation.
The system architecture is scalable and can handle larger datasets when transcripts are available.

▶️ How to Run the Project

Open the notebook in Google Colab or Jupyter Notebook

Add your YouTube Data API key

Run cells step by step

Launch the Gradio interface

Enter a query to search videos semantically

📊 Example Query
Explain arrays in JavaScript


The system returns the most relevant videos ranked by semantic similarity.

✅ Project Status

Video extraction ✔️

Transcript extraction ✔️

Embedding generation ✔️

Semantic search ✔️

Interactive UI ✔️

👤 Author

Aditya Vishwakarma
Intern – Infosys Springboard
