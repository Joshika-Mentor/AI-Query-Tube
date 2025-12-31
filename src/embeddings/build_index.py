import argparse
import pandas as pd
import numpy as np
import os
from loguru import logger
import sys

# Fix imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.embeddings.embed_models import load_model

def build_index(data_path, model_name, out_index_path, out_emb_path):
    if not os.path.exists(data_path):
        logger.error(f"Data file {data_path} not found.")
        return

    logger.info(f"Loading data from {data_path}...")
    df = pd.read_parquet(data_path)
    
    logger.info(f"Loading model {model_name}...")
    embedder = load_model(model_name)
    
    logger.info("Encoding phrases...")
    embeddings = embedder.encode(df["text"].tolist(), show_progress_bar=True)
    
    logger.info(f"Saving embeddings to {out_emb_path}...")
    os.makedirs(os.path.dirname(out_emb_path), exist_ok=True)
    np.save(out_emb_path, embeddings)
    
    logger.info(f"Saving dataframe index to {out_index_path}...")
    df.to_parquet(out_index_path, index=False)
    
    logger.success("Index build complete.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--model_name", default="all-MiniLM-L6-v2")
    parser.add_argument("--out_index", required=True)
    parser.add_argument("--out_embeddings", required=True)
    args = parser.parse_args()
    
    build_index(args.data, args.model_name, args.out_index, args.out_embeddings)

if __name__ == "__main__":
    main()
