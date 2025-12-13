import argparse
import pandas as pd
import numpy as np
import os
from src.embeddings.embed_models import Embedder
import faiss

def build_index(data_path, model_name, output_dir):
    df = pd.read_parquet(data_path)
    print(f"Loading model {model_name}...")
    embedder = Embedder(model_name)
    
    print(f"Embedding {len(df)} documents...")
    embeddings = embedder.encode(df['text_to_embed'].tolist())
    
    # Save Embeddings
    os.makedirs(output_dir, exist_ok=True)
    np.save(os.path.join(output_dir, "video_embeddings.npy"), embeddings)
    
    # Build FAISS Index (L2 or InnerProduct? sentence-transformers often normalized -> InnerProduct == Cosine)
    d = embeddings.shape[1]
    # Use Inner Product (since normalized)
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    
    faiss.write_index(index, os.path.join(output_dir, "video_index.faiss"))
    
    # Save metadata/mapping
    df.reset_index(drop=True).to_parquet(os.path.join(output_dir, "video_index.parquet"))
    
    print(f"Index built and saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/clean_videos.parquet")
    parser.add_argument("--model", default="all-MiniLM-L6-v2")
    parser.add_argument("--out_dir", default="data/")
    
    args = parser.parse_args()
    build_index(args.data, args.model, args.out_dir)
