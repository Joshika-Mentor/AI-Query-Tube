import numpy as np
import faiss

def search_faiss(query_vector, index, top_k=5):
    """
    Search using FAISS index.
    Returns (distances, variables)
    """
    if len(query_vector.shape) == 1:
        query_vector = query_vector.reshape(1, -1)
    
    # Normalize if using Inner Product (Cosine)
    faiss.normalize_L2(query_vector)
    
    distances, indices = index.search(query_vector, top_k)
    return distances[0], indices[0]

def compute_similarity(query_emb, doc_embs, metric='cosine'):
    # Fallback if no FAISS
    # Implementation optional if FAISS is primary
    pass
