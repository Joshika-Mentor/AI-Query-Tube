import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

print("🚀 Regenerating improved embeddings...")

df = pd.read_csv("data/videos_multi_clean.csv")

# 🔥 IMPROVED TEXT
df["embed_text"] = df["title"] + " | " + df["channel_name"]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["embed_text"].tolist(), show_progress_bar=True)

np.save("data/title_embeddings_multi.npy", embeddings)

print("✅ Improved embeddings saved")
