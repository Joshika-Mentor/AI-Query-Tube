print("SCRIPT STARTED (SEMANTIC SEARCH - MULTI-CHANNEL)")

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# -------- Load cleaned dataset --------
DATA_PATH = "data/videos_multi_clean.csv"
df = pd.read_csv(DATA_PATH)

print(f"\n📌 Loaded {len(df)} videos for semantic search")

# -------- Text Normalization (must match Milestone-2) --------
df["title"] = df["title"].astype(str).str.strip().str.lower()
df["channel_name"] = df["channel_name"].astype(str).str.strip()

# -------- Load embedding model --------
print("\n🔄 Loading SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- Generate embeddings --------
print("\n🧠 Generating title embeddings...")
embeddings = model.encode(
    df["title"].tolist(),
    show_progress_bar=True
)

print("Embeddings shape:", embeddings.shape)

# -------- Save embeddings --------
os.makedirs("data", exist_ok=True)
np.save("data/title_embeddings_multi.npy", embeddings)

print("💾 Embeddings saved → data/title_embeddings_multi.npy")

# -------- Semantic search function --------
def search_videos(query, top_k=5):
    query = str(query).lower().strip()
    query_vec = model.encode([query])
    similarities = cosine_similarity(query_vec, embeddings)[0]

    top_indices = similarities.argsort()[::-1][:top_k]

    return df.iloc[top_indices][
        ["video_id", "title", "channel_name", "publishedAt"]
    ]

# -------- Test semantic search --------
print("\n🔎 TEST SEARCH RESULT:")
test_results = search_videos("tamil songs")
print(test_results)

print("\n✅ Milestone 3 (Semantic Search) Completed Successfully!")
