import gradio as gr
from src.search.query_service import SearchEngine
import os

# Initialize Engine Global
# Check if data exists
if not os.path.exists("data/video_index.faiss"):
    print("WARNING: Index not found. App will fail to search.")
    engine = None
else:
    engine = SearchEngine()

def search(query):
    if not engine:
        return "Index not built. Please run build_index.py first."
    
    results = engine.search(query, top_k=5)
    
    output_html = ""
    for res in results:
        score_display = f"{res['score']:.4f}"
        
        # Card HTML
        card = f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; display: flex;">
            <div style="flex: 0 0 150px; margin-right: 15px;">
                <img src="{res['thumbnail']}" style="width: 100%; border-radius: 4px;">
            </div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 5px;"><a href="{res['url']}" target="_blank">{res['title']}</a></h3>
                <p style="margin: 0; color: #666; font-size: 0.9em;">Score: {score_display} | Published: {res['publish_date']}</p>
                <p style="margin: 5px 0 0; font-size: 0.9em;">{res['description'][:200]}...</p>
            </div>
        </div>
        """
        output_html += card
    
    return output_html

with gr.Blocks(title="QueryTube") as demo:
    gr.Markdown("# QueryTube: AI Semantic Search for YouTube")
    
    with gr.Row():
        query_input = gr.Textbox(label="Enter your query", placeholder="e.g., machine learning tutorial")
        search_btn = gr.Button("Search", variant="primary")
        
    results_output = gr.HTML(label="Results")
    
    # Examples
    examples = []
    if os.path.exists("assets/sample_queries.txt"):
        with open("assets/sample_queries.txt") as f:
            examples = [[line.strip()] for line in f.readlines()[:10] if line.strip()]
            
    gr.Examples(examples=examples, inputs=query_input)
    
    search_btn.click(fn=search, inputs=query_input, outputs=results_output)
    query_input.submit(fn=search, inputs=query_input, outputs=results_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
