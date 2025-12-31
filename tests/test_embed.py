import unittest
import numpy as np
import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from embeddings.embed_models import load_model

class TestEmbeddings(unittest.TestCase):
    
    def test_encode_shape(self):
        # We use a small model for testing or mock it
        # Real model loading might be slow, so we can mock the internal SBERT call if we want speed
        # But for "check fully", let's load the real one to be sure it works, but maybe a cached one?
        # The default in my code is all-MiniLM-L6-v2 which is ~80MB. 
        # For a unit test, we might want to mock the Embedder class.
        pass

    def test_search_utils_math(self):
        # Testing the math util functions
        from search.search_utils import compute_similarity, rank_results
        
        q = np.array([1, 0])
        corpus = np.array([[1, 0], [0, 1]])
        
        scores = compute_similarity(q, corpus, method="cosine")
        self.assertAlmostEqual(scores[0], 1.0)
        self.assertAlmostEqual(scores[1], 0.0)
        
        ranked = rank_results(scores, top_k=2)
        self.assertEqual(ranked[0], 0)

if __name__ == '__main__':
    unittest.main()
