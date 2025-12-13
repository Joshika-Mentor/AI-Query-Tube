import pytest
import numpy as np
from src.embeddings.embed_models import Embedder

@pytest.fixture(scope="module")
def embedder():
    return Embedder('all-MiniLM-L6-v2', device='cpu')

def test_embedder_shape(embedder):
    texts = ["hello", "world"]
    embeddings = embedder.encode(texts)
    assert len(embeddings) == 2
    assert embeddings.shape[1] == 384 # Known dim for this model

def test_embedder_normalization(embedder):
    texts = ["test"]
    emb = embedder.encode(texts)[0]
    norm = np.linalg.norm(emb)
    # allow small float error
    assert abs(norm - 1.0) < 1e-5
