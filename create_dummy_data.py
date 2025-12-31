import pandas as pd
import os

def create_dummy_data(out_path):
    data = [
        {
            "video_id": "vid1",
            "title": "Introduction to Machine Learning",
            "publish_date": "2023-01-01",
            "text": "machine learning introduction tutorial basics ai artificial intelligence",
            "youtube_url": "https://www.youtube.com/watch?v=vid1",
            "description": "A basic intro to ML."
        },
        {
            "video_id": "vid2", 
            "title": "Python for Data Science",
            "publish_date": "2023-01-02",
            "text": "python programming data science pandas numpy matplotlib tutorial",
            "youtube_url": "https://www.youtube.com/watch?v=vid2",
            "description": "Learn Python for data analysis."
        },
        {
            "video_id": "vid3",
            "title": "Semantic Search with Transformers",
            "publish_date": "2023-01-03",
            "text": "semantic search embeddings bert transformers nlp natural language processing",
            "youtube_url": "https://www.youtube.com/watch?v=vid3",
            "description": "Building search engines with vector databases."
        }
    ]
    
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_parquet(out_path, index=False)
    print(f"Created dummy data at {out_path}")

if __name__ == "__main__":
    create_dummy_data("data/clean_videos.parquet")
