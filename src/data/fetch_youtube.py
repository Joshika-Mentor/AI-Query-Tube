import os
import argparse
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

def get_channel_videos(api_key, channel_id, start_date=None, max_results=350):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # 1. Get Uploads Playlist ID
        channel_response = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        ).execute()
        
        if not channel_response.get('items'):
            print(f"Error: Channel ID {channel_id} not found.")
            return []
            
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        videos = []
        next_page_token = None
        
        pbar = tqdm(total=max_results, desc="Fetching Videos")
        
        while len(videos) < max_results:
            try:
                playlist_response = youtube.playlistItems().list(
                    playlistId=uploads_playlist_id,
                    part='snippet,contentDetails',
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                items = playlist_response.get('items', [])
                if not items:
                    break
                
                for item in items:
                    snippet = item['snippet']
                    video_id = snippet['resourceId']['videoId']
                    
                    # Basic filtering if needed (e.g. shorts vs full videos? For now, take all)
                    
                    videos.append({
                        'video_id': video_id,
                        'title': snippet['title'],
                        'publish_date': snippet['publishedAt'],
                        'description': snippet['description'],
                        'thumbnail': snippet['thumbnails'].get('high', {}).get('url', '')
                    })
                    pbar.update(1)
                    
                    if len(videos) >= max_results:
                        break
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            except HttpError as e:
                print(f"An error occurred: {e}")
                break
                
        pbar.close()
        return videos

    except Exception as e:
        print(f"Critical error: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube Video Metadata")
    parser.add_argument("--api_key", help="YouTube Data API Key", default=os.getenv("YT_API_KEY"))
    parser.add_argument("--channel_id", help="YouTube Channel ID", default=os.getenv("CHANNEL_ID"))
    parser.add_argument("--out", help="Output parquet file", default="data/raw_videos.parquet")
    parser.add_argument("--max_videos", help="Max videos to fetch", type=int, default=350)
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set YT_API_KEY env var or pass --api_key")
        return
        
    if not args.channel_id:
        print("Error: Channel ID is required. Set CHANNEL_ID env var or pass --channel_id")
        return

    print(f"Fetching up to {args.max_videos} videos for channel {args.channel_id}...")
    video_data = get_channel_videos(args.api_key, args.channel_id, max_results=args.max_videos)
    
    if video_data:
        df = pd.DataFrame(video_data)
        # Ensure output directory exists
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        df.to_parquet(args.out, index=False)
        print(f"Success! Saved {len(df)} videos to {args.out}")
        print(df.head())
    else:
        print("No videos found or fetch failed.")

if __name__ == "__main__":
    main()
