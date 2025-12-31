from sentence_transformers import SentenceTransformer
import numpy as np
import torch
from loguru import logger

class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2', device=None):
        self.model_name = model_name
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
            
        logger.info(f"Loading model {model_name} on {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)
        
    def encode(self, texts, batch_size=32, show_progress_bar=True):
        """
        Embeds a list of texts.
        Returns numpy array of shape (n_texts, embedding_dim)
        """
        embeddings = self.model.encode(
            texts, 
            batch_size=batch_size, 
            show_progress_bar=show_progress_bar, 
            convert_to_numpy=True,
            normalize_embeddings=True # Important for cosine similarity
        )
        return embeddings

def load_model(model_name="all-MiniLM-L6-v2"):
    return Embedder(model_name)

if __name__ == "__main__":
    # Test
    e = Embedder()
    res = e.encode(["Hello world", "Machine learning"])
    print(res.shape)
