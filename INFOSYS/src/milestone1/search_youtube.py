"""
YouTube Search Functionality
Searches YouTube videos using the YouTube Data API v3.
"""

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeSearcher:
    """Handles YouTube video searches using the YouTube Data API."""
    
    def __init__(self, api_key=None):
        """
        Initialize the YouTube API client.
        
        Args:
            api_key (str): YouTube Data API key. If None, loads from .env file.
        """
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found. Please set YOUTUBE_API_KEY in .env file.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def get_channel_id(self, channel_name):
        """
        Get channel ID from channel name or handle.
        
        Args:
            channel_name (str): Channel name or handle (e.g., @channelname)
            
        Returns:
            str: Channel ID or None if not found
        """
        try:
            # Search for the channel
            request = self.youtube.search().list(
                part='snippet',
                q=channel_name,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]['snippet']['channelId']
            return None
        except Exception as e:
            print(f"Error finding channel: {e}")
            return None
    
    def search_videos(self, query, max_results=10, channel_id=None):
        """
        Search for YouTube videos, optionally within a specific channel.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return (default: 10)
            channel_id (str): Optional channel ID to search within
            
        Returns:
            list: List of dictionaries containing video information:
                - video_id: YouTube video ID
                - title: Video title
                - channel: Channel name
                - description: Video description
        """
        try:
            # Call the YouTube API
            search_params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'relevanceLanguage': 'en',
                'videoCaption': 'any'
            }
            
            # Add channel filter if provided
            if channel_id:
                search_params['channelId'] = channel_id
            
            request = self.youtube.search().list(**search_params)
            response = request.execute()
            
            # Extract video information
            videos = []
            for item in response.get('items', []):
                video_info = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description']
                }
                videos.append(video_info)
            
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []
