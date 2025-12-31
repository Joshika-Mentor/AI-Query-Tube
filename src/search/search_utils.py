import numpy as np
import faiss
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

def search_faiss(query_vector, index, top_k=5):
    """
    Search using FAISS index.
    Returns (distances, variables)
    """
    if len(query_vector.shape) == 1:
        query_vector = query_vector.reshape(1, -1)
    
    # Normalize if using Inner Product (Cosine)
    # Note: embedder should normalize, but doing it here is safe provided index is IP
    faiss.normalize_L2(query_vector)
    
    distances, indices = index.search(query_vector, top_k)
    return distances[0], indices[0]

def compute_similarity(query_emb, doc_embs, method='cosine'):
    if len(query_emb.shape) == 1:
        query_emb = query_emb.reshape(1, -1)
    
    if method == 'cosine':
        return cosine_similarity(query_emb, doc_embs)[0]
    elif method == 'euclidean':
        # Return negative distance so higher is better? 
        # Usually search expects similarity.
        dists = euclidean_distances(query_emb, doc_embs)[0]
        return 1 / (1 + dists) # Simple similarity conversion
    else:
        raise ValueError(f"Unknown method {method}")

def rank_results(scores, top_k=5):
    """
    Returns indices of top_k highest scores.
    """
    indices = np.argsort(scores)[::-1]
    return indices[:top_k]
