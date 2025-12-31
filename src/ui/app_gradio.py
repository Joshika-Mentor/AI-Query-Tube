import gradio as gr
import argparse
import os
import sys

# Ensure we can import from src regardless of where this script is run
# Add the project root (../../) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.search.query_service import VideoSearcher, returnSearchResults

SEARCHER = None

def search_fn(query):
    if not query:
        return "Please enter a query."
    
    if SEARCHER is None:
        return "Search engine not initialized. Please run build_index.py first."

    # returnSearchResults returns a list of specific dicts
    results = returnSearchResults(query, SEARCHER, top_k=5)
    
    if not results:
        return "No results found."
    
    html_output = ""
    for r in results:
        vid = r.get('video_id', '')
        title = r.get('title', 'Unknown Title')
        score = r.get('score', 0.0)
        date = r.get('publish_date', '')
        text = r.get('text', '')
        url = r.get('youtube_url', f"https://www.youtube.com/watch?v={vid}")
        thumb = f"https://img.youtube.com/vi/{vid}/0.jpg"
        
        display_score = f"{score:.4f}"
        
        html_output += f"""
        <div style="display: flex; margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; border-radius: 8px;">
            <div style="flex: 0 0 200px; margin-right: 20px;">
                <a href="{url}" target="_blank">
                    <img src="{thumb}" style="width: 100%; border-radius: 4px;">
                </a>
            </div>
            <div style="flex: 1;">
                <h3 style="margin-top: 0; margin-bottom: 5px;"><a href="{url}" target="_blank" style="text-decoration: none; color: #333;">{title}</a></h3>
                <p style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Published: {date} | Score: {display_score}</p>
                <p style="font-size: 0.95em;">{text}</p>
            </div>
        </div>
        """
    return html_output

def load_example_queries():
    path = os.path.join(project_root, 'assets/sample_queries.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return [line.strip() for line in f if line.strip()][:10]
    return []

def main():
    parser = argparse.ArgumentParser()
    # Use absolute paths relative to project root for defaults
    default_index = os.path.join(project_root, "data/video_index.parquet")
    default_emb = os.path.join(project_root, "data/video_embeddings.npy")
    
    parser.add_argument("--index", default=default_index)
    parser.add_argument("--embeddings", default=default_emb)
    parser.add_argument("--model_name", default="all-MiniLM-L6-v2")
    parser.add_argument("--share", action="store_true")
    args = parser.parse_args()
    
    global SEARCHER
    if os.path.exists(args.index) and os.path.exists(args.embeddings):
        SEARCHER = VideoSearcher(args.index, args.embeddings, args.model_name)
    else:
        print(f"WARNING: Index files not found at {args.index} or {args.embeddings}")
        print("Please run src/embeddings/build_index.py first.")
    
    examples = load_example_queries()
    
    with gr.Blocks(title="QueryTube") as demo:
        gr.Markdown("# QueryTube: Semantic Search for YouTube")
        gr.Markdown("Search for videos using natural language.")
        
        with gr.Row():
            inp = gr.Textbox(placeholder="Enter your query...", label="Query", lines=1)
            btn = gr.Button("Search", variant="primary")
            
        out = gr.HTML(label="Results")
        
        if examples:
            gr.Examples(examples, inp)
            
        inp.submit(search_fn, inp, out)
        btn.click(search_fn, inp, out)
        
    demo.launch(server_name="0.0.0.0", server_port=7860, share=args.share)

if __name__ == "__main__":
    main()
