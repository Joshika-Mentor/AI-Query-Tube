from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once
model = SentenceTransformer("all-mpnet-base-v2")

def rank_videos(query: str, videos: list):
    texts = []
    for v in videos:
        text = v["title"]
        if v.get("transcript"):
            text += " " + v["transcript"]
        texts.append(text)

    video_embeddings = model.encode(texts)
    query_embedding = model.encode([query])

    scores = cosine_similarity(query_embedding, video_embeddings)[0]
    ranked_idx = np.argsort(scores)[::-1]

    results = []
    for idx in ranked_idx:
        v = videos[idx]
        v["score"] = float(scores[idx])
        results.append(v)

    return results
