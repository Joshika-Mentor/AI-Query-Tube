# QueryTube Architecture

## Overview
QueryTube is a semantic search engine designed to index and search YouTube videos based on their transcripts and metadata. It uses a vector-based retrieval approach.

## Components

### 1. Data Collection (`src/data`)
- **fetch_youtube.py**: Interacts with YouTube Data API v3. Handles pagination to retrieve video metadata (Title, ID, Description, Date) from the 'Uploads' playlist of a channel.
- **fetch_transcripts.py**: Uses `youtube_transcript_api` to download subtitles/captions.
- **preprocess.py**: Cleanses text (lowercasing, punctuation) and constructs the final text blob for embedding (Title + Transcript).

### 2. Embeddings (`src/embeddings`)
- **embed_models.py**: Wrapper around `sentence-transformers`. Defaults to `all-MiniLM-L6-v2` for speed/performance balance.
- **build_index.py**: Inference step. Converts the cleaned dataset into vectors and saves them.
- **Index Storage**: 
  - `video_index.faiss`: Efficient similarity search index (FAISS).
  - `video_embeddings.npy`: Raw numpy array (backup).
  - `video_index.parquet`: Metadata corresponding to the vectors.

### 3. Search Service (`src/search`)
- **query_service.py**: Loading the index and handling search requests.
- **Logic**:
  1. Encode User Query -> Vector.
  2. FAISS Inner Product Search -> Top K Indices.
  3. Retrieve Metadata -> Return JSON-like objects.

### 4. User Interface (`src/ui`)
- **app_gradio.py**: A web frontend using Gradio. Displays results with thumbnails and links.

## Data Flow
Youtube API -> Raw Parquet -> Transcripts Parquet -> Clean Parquet -> Vector Index -> Search UI
