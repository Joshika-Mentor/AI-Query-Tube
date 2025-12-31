import pandas as pd
import numpy as np
import os
import sys
from loguru import logger

# Fix imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try imports
try:
    from src.embeddings.embed_models import load_model
    from src.search.search_utils import compute_similarity, rank_results
except ImportError:
    # If generic src import fails, try relative if somehow in path
    from embeddings.embed_models import load_model
    from search.search_utils import compute_similarity, rank_results

class VideoSearcher:
    def __init__(self, index_path, embeddings_path, model_name="all-MiniLM-L6-v2"):
        logger.info("Initializing VideoSearcher...")
        self.index_path = index_path
        self.embeddings_path = embeddings_path
        self.model_name = model_name
        
        self.df = None
        self.embeddings = None
        self.embedder = None
        
        self._load_resources()
        
    def _load_resources(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.embeddings_path):
            logger.error(f"Index or embeddings file not found: {self.index_path}, {self.embeddings_path}")
            return

        logger.info(f"Loading index from {self.index_path}")
        self.df = pd.read_parquet(self.index_path)
        
        logger.info(f"Loading embeddings from {self.embeddings_path}")
        self.embeddings = np.load(self.embeddings_path)
        
        self.embedder = load_model(self.model_name)
        logger.success("Resources loaded.")

    def search(self, query, top_k=5, threshold=0.0):
        if self.embeddings is None or self.embedder is None:
            logger.error("Searcher not initialized properly.")
            return []

        # Encode query
        query_emb = self.embedder.encode(query, show_progress_bar=False)
        
        # Compute scores (Cosine is standard default)
        scores = compute_similarity(query_emb, self.embeddings, method="cosine")
        
        # Rank
        ranked_indices = rank_results(scores, top_k=top_k * 2) # Get more to filter
        
        results = []
        for idx in ranked_indices:
            score = scores[idx]
            if score < threshold:
                continue
            
            # Use safe access .get for columns
            if idx < len(self.df):
                row = self.df.iloc[idx]
                result = {
                    "video_id": row.get("video_id", "N/A"),
                    "title": row.get("title", "No Title"),
                    "publish_date": row.get("publish_date", ""),
                    "score": float(score),
                    "youtube_url": row.get("youtube_url", f"https://www.youtube.com/watch?v={row.get('video_id', '')}"),
                    "text": row.get("text", "")[:200] + "..." # Snippet
                }
                results.append(result)
            
            if len(results) >= top_k:
                break
                
        return results

def returnSearchResults(query, searcher, top_k=5):
    """
    Wrapper function as requested in requirements.
    """
    if searcher is None:
        return []
    return searcher.search(query, top_k=top_k)
