import argparse
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from tqdm import tqdm
import os

def fetch_transcripts(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return

    df = pd.read_parquet(input_file)
    print(f"Loaded {len(df)} videos from {input_file}")
    
    results = []
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Fetching Transcripts"):
        video_id = row['video_id']
        result = {
            'video_id': video_id,
            'title': row['title'],
            'publish_date': row['publish_date'],
            'transcript': "",
            'transcript_available': False,
            'error': None
        }
        
        try:
            # Fetch transcript (English preferred, auto-generated acceptable)
            # Instantiate API (Note: In loop might be less efficient but safe)
            api = YouTubeTranscriptApi() 
            transcript_list = api.fetch(video_id, languages=['en', 'en-US'])
            
            # Combine text (handle object attributes)
            full_text = " ".join([t.text for t in transcript_list])
            
            result['transcript'] = full_text
            result['transcript_available'] = True
            
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            result['error'] = "No transcript available"
        except Exception as e:
            # Fallback for old API just in case or other errors
            if "has no attribute 'fetch'" in str(e):
                 # Try static method logic for backward compat? No, assume new.
                 pass
            result['error'] = str(e)
            
        results.append(result)
        
    out_df = pd.DataFrame(results)
    
    # Preserve original metadata if needed, or just keep what we have
    # Let's merge/ensure we have all columns from input that we might care about?
    # For now, just using the structure defined in requirements.
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    out_df.to_parquet(output_file, index=False)
    print(f"Saved transcripts to {output_file}. Available: {out_df['transcript_available'].sum()}/{len(out_df)}")

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube Transcripts")
    parser.add_argument("--in_file", help="Input raw videos parquet", default="data/raw_videos.parquet")
    parser.add_argument("--out", help="Output transcripts parquet", default="data/transcripts.parquet")
    
    args = parser.parse_args()
    fetch_transcripts(args.in_file, args.out)

if __name__ == "__main__":
    main()
