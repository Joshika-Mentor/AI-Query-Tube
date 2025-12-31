# SmartTube: AI Semantic Search for YouTube

SmartTube is a local semantic search engine that allows you to search through a YouTube channel's videos using natural language. It indexes video transcripts and metadata to find the most relevant content.

## Features
- **Semantic Search**: Find videos by meaning, not just keywords.
- **Transcript Indexing**: Searches through the actual spoken content of videos.
- **Model Evaluation**: Compare different embedding models.
- **Gradio UI**: Simple web interface for searching.

## Setup

1. **Clone the repository** (or download the files).
2. **Install Dependencies**:
   You can install the package and its dependencies using pip:
   ```bash
   pip install -e .
   ```
   Or strictly from requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Setup**:
   Create a `.env` file in the root directory (copy from `.env.example`).
   ```bash
   YT_API_KEY=your_api_key
   CHANNEL_ID=your_channel_id
   ```

## Usage Pipeline

### 1. Data Collection
Fetch video metadata and transcripts.
```bash
python src/data/fetch_youtube.py
python src/data/fetch_transcripts.py
python src/data/preprocess.py
```

### 2. Build Index
Generate embeddings and build the FAISS index.
```bash
python src/embeddings/build_index.py --model all-MiniLM-L6-v2
```

### 3. Run Search App
Launch the Gradio interface.
```bash
python src/ui/app_gradio.py
```
Open your browser at `http://localhost:7860`.

### (Optional) Evaluation
Evaluate different models.
```bash
python src/embeddings/evaluate_models.py
```

## Docker
Build and run using Docker:
```bash
docker build -t querytube .
docker run -p 7860:7860 querytube
```

## Architecture
See [docs/architecture.md](docs/architecture.md) for details.
