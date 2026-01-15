import pandas as pd
import numpy as np
import gradio as gr
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("🚀 Starting QueryTube Gradio App...")

# ======================
# Load data and embeddings
# ======================
df = pd.read_csv("data/videos_multi_clean.csv")
embeddings = np.load("data/title_embeddings_multi.npy")

print("✅ Data loaded successfully")
print("Columns:", df.columns)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ======================
# Semantic + Hybrid Search
# ======================
def semantic_search(query):
    try:
        query = str(query).lower().strip()
        query_embedding = model.encode([query])

        semantic_scores = cosine_similarity(query_embedding, embeddings)[0]
        boosted_scores = []

        # Domain keywords
        music_keywords = ["song", "songs", "music", "bollywood", "lyrics"]
        food_keywords = ["food", "cooking", "recipe", "village"]
        movie_keywords = ["movie", "film", "cinema", "trailer"]
        education_keywords = ["python", "java", "tutorial", "course", "learn"]

        for idx, row in df.iterrows():
            score = semantic_scores[idx]

            title = str(row.get("title", "")).lower()
            channel = str(row.get("channel_name", "")).lower()

            # Keyword boosting
            for word in query.split():
                if word in title:
                    score += 0.25
                if word in channel:
                    score += 0.15

            # 🔥 DOMAIN BOOSTING
            if any(k in query for k in music_keywords) and "music" in channel:
                score += 0.8

            if any(k in query for k in food_keywords) and "cooking" in channel:
                score += 0.8

            if any(k in query for k in movie_keywords) and "cine" in channel:
                score += 0.8

            if any(k in query for k in education_keywords) and channel in [
                "freecodecamp",
                "error makes clever"
            ]:
                score += 0.8

            # 🚫 DOMAIN PENALTY (important)
            if any(k in query for k in music_keywords) and "music" not in channel:
                score -= 0.6

            if any(k in query for k in food_keywords) and "cooking" not in channel:
                score -= 0.6

            if any(k in query for k in movie_keywords) and "cine" not in channel:
                score -= 0.6

            if any(k in query for k in education_keywords) and channel not in [
                "freecodecamp",
                "error makes clever"
            ]:
                score -= 0.6

            boosted_scores.append(score)

        top_indices = np.argsort(boosted_scores)[::-1][:5]
        results = df.iloc[top_indices]

        html_output = ""
        for _, row in results.iterrows():
            title = str(row.get("title", "No Title")).strip()
            channel = str(row.get("channel_name", "Unknown Channel")).strip()
            video_id = str(row.get("video_id", "")).strip()

            if not video_id:
                continue

            html_output += f"""
            <div style="margin-bottom:25px">
              <h4>{title}</h4>
              <p><b>Channel:</b> {channel}</p>
              <iframe
              style="width:100%; max-width:560px; height:315px;"
              src="https://www.youtube-nocookie.com/embed/{video_id}"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen>
            </iframe>

            <p>
              <a href="https://www.youtube.com/watch?v={video_id}" target="_blank">
              ▶ Watch on YouTube
              </a>
            </p>

            </div>
            <hr>
            """

        return html_output if html_output else "<b>No results found.</b>"

    except Exception as e:
        return f"<b>⚠ Error:</b><br>{str(e)}"

# ======================
# Gradio UI
# ======================
with gr.Blocks() as demo:
    gr.Markdown("## 🔍 QueryTube – Multi-Domain YouTube Semantic Search")
    gr.Markdown(
        "Search across **Education, Food, Songs, and Movies** using semantic intelligence."
    )

    query = gr.Textbox(
        label="Enter your search query",
        placeholder="e.g. python tutorial, bollywood song, village cooking"
    )

    output = gr.HTML()
    query.submit(semantic_search, query, output)

demo.launch()
