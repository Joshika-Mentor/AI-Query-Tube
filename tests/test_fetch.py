import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from data.fetch_youtube import fetch_videos

class TestFetch(unittest.TestCase):

    @patch('data.fetch_youtube.build')
    def test_fetch_videos_mock(self, mock_build):
        mock_youtube = MagicMock()
        mock_build.return_value = mock_youtube
        
        # Mock channels response
        mock_youtube.channels().list().execute.return_value = {
            "items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UU123"}}}]
        }
        
        # Mock playlist response
        mock_youtube.playlistItems().list().execute.return_value = {
            "items": [{
                "snippet": {
                    "resourceId": {"videoId": "vid1"},
                    "title": "Test Video",
                    "description": "Desc",
                    "publishedAt": "2023-01-01",
                    "channelId": "UC123",
                    "channelTitle": "Test Channel"
                }
            }],
            "nextPageToken": None
        }
        
        videos = fetch_videos("fake_key", "UC123", max_results=1)
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0]["video_id"], "vid1")

if __name__ == '__main__':
    unittest.main()
