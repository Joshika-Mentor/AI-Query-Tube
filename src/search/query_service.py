import pandas as pd
import numpy as np
import faiss
from src.embeddings.embed_models import Embedder
from src.search.search_utils import search_faiss
import os

class SearchEngine:
    def __init__(self, index_path="data/video_index.faiss", meta_path="data/video_index.parquet", model_name="all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.meta_path = meta_path
        
        print("Loading metadata...")
        self.df = pd.read_parquet(meta_path)
        
        print("Loading index...")
        self.index = faiss.read_index(index_path)
        
        print(f"Loading model {model_name}...")
        self.embedder = Embedder(model_name)
        
    def search(self, query, top_k=5, threshold=0.0):
        # Encode
        query_emb = self.embedder.encode([query])
        
        # Search
        scores, indices = search_faiss(query_emb, self.index, top_k=top_k)
        
        results = []
        for score, idx in zip(scores, indices):
            if idx == -1: continue
            if score < threshold: continue
            
            row = self.df.iloc[idx]
            results.append({
                'video_id': row['video_id'],
                'title': row['title'],
                'publish_date': row['publish_date'],
                'score': float(score),
                'url': f"https://www.youtube.com/watch?v={row['video_id']}",
                'thumbnail': f"https://img.youtube.com/vi/{row['video_id']}/0.jpg",
                'description': row.get('description', '')
            })
            
        return results

def returnSearchResults(query, engine, top_k=5):
    # Wrapper as requested
    return engine.search(query, top_k)
