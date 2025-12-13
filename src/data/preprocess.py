import pandas as pd
import argparse
import re
import os
import string

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove emojis (simple regex for non-ascii approx)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove repeated punctuation
    text = re.sub(r'([!?,.])\1+', r'\1', text)
    
    return text

def preprocess_data(input_file, output_file, mode='combined'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    df = pd.read_parquet(input_file)
    print(f"Loaded {len(df)} records.")
    
    # Filter only available transcripts
    df = df[df['transcript_available'] == True].copy()
    print(f"Filtering to {len(df)} videos with transcripts.")
    
    # Clean fields
    df['clean_title'] = df['title'].apply(clean_text)
    df['clean_transcript'] = df['transcript'].apply(clean_text)
    
    # Create text to embed
    if mode == 'title_only':
        df['text_to_embed'] = df['clean_title']
    elif mode == 'transcript_only':
        df['text_to_embed'] = df['clean_transcript']
    else: # combined
        # Give title some weight/presence? Just concatenation for now.
        df['text_to_embed'] = "Title: " + df['clean_title'] + " Content: " + df['clean_transcript']
        
    # Truncate if too long? SentenceTransformers handle truncation usually, 
    # but for search index, we might chunk. For now, we embed the whole thing (average 10-20 min video)
    # Note: 512 token limit for standard BERT models. 
    # For a naive implementation, we'll just let the model truncate or we should chunk.
    # The requirement says "build an embedding index". It doesn't explicitly force chunking,
    # but for 20 min videos, the transcript is HUGE.
    # The prompt says: "extract video metadata + transcripts ... embed texts ... return top-5 relevant video titles".
    # It implies video-level retrieval.
    # We will truncate to first N chars or use a model that supports longer context if possible, 
    # but 'all-MiniLM-L6-v2' is 512 tokens.
    # We will slice the transcript to the first ~1000 words (approx 5-7 mins of speech) or just the description + first part.
    # Let's keep it simple for now: Title + Description + First 4000 chars of transcript?
    
    df['text_to_embed'] = df['text_to_embed'].str.slice(0, 8000) # Safety cap
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_parquet(output_file, index=False)
    print(f"Saved preprocessed data to {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_file", default="data/transcripts.parquet")
    parser.add_argument("--out", default="data/clean_videos.parquet")
    parser.add_argument("--mode", choices=['title_only', 'transcript_only', 'combined'], default='combined')
    
    args = parser.parse_args()
    preprocess_data(args.in_file, args.out, args.mode)

if __name__ == "__main__":
    main()
