import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from search.query_service import VideoSearcher

class TestVideoSearcher(unittest.TestCase):
    
    @patch('search.query_service.load_model')
    @patch('pandas.read_parquet')
    @patch('numpy.load')
    @patch('os.path.exists')
    def test_search_flow(self, mock_exists, mock_np_load, mock_read_parquet, mock_load_model):
        mock_exists.return_value = True
        
        # Mock Index
        mock_df = pd.DataFrame([{
            "video_id": "v1", "title": "Test Title", "publish_date": "2023", "text": "Content", "youtube_url": "http"
        }])
        mock_read_parquet.return_value = mock_df
        
        # Mock Embeddings
        mock_emb = np.array([[0.9, 0.1]])
        mock_np_load.return_value = mock_emb
        
        # Mock Model
        mock_embedder = MagicMock()
        mock_embedder.encode.return_value = np.array([0.9, 0.1])
        mock_load_model.return_value = mock_embedder
        
        searcher = VideoSearcher("idx", "emb")
        results = searcher.search("query", top_k=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["video_id"], "v1")
        # Dot product of [0.9, 0.1] with itself is 0.81+0.01 = 0.82? No, cosine similarity of identical vectors is 1.0
        # Wait, compute_similarity uses cosine_similarity from sklearn
        self.assertAlmostEqual(results[0]["score"], 1.0)

if __name__ == '__main__':
    unittest.main()
