import pytest
from unittest.mock import MagicMock, patch
from src.data.fetch_youtube import get_channel_videos

@patch('src.data.fetch_youtube.build')
def test_get_channel_videos_success(mock_build):
    # Mock invalid API Setup
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    
    # Mock Channels List Response
    mock_channels = mock_youtube.channels().list().execute
    mock_channels.return_value = {
        'items': [{'contentDetails': {'relatedPlaylists': {'uploads': 'UU_PLAYLIST_ID'}}}]
    }
    
    # Mock PlaylistItems Response
    mock_playlist = mock_youtube.playlistItems().list().execute
    mock_playlist.return_value = {
        'items': [
            {
                'snippet': {
                    'resourceId': {'videoId': 'vid123'},
                    'title': 'Test Video',
                    'publishedAt': '2023-01-01T00:00:00Z',
                    'description': 'Desc',
                    'thumbnails': {'high': {'url': 'http://img.jpg'}}
                }
            }
        ],
        'nextPageToken': None
    }
    
    videos = get_channel_videos('FAKE_KEY', 'CHANNEL_ID', max_results=5)
    
    assert len(videos) == 1
    assert videos[0]['video_id'] == 'vid123'
    assert videos[0]['title'] == 'Test Video'

@patch('src.data.fetch_youtube.build')
def test_get_channel_videos_not_found(mock_build):
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    
    # Empty items
    mock_youtube.channels().list().execute.return_value = {'items': []}
    
    videos = get_channel_videos('FAKE_KEY', 'BAD_ID')
    assert videos == []
