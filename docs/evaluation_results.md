# Evaluation Results

This document summarizes the performance of different sentence embedding models for the QueryTube semantic search engine.

## Methodology
We evaluated models using a set of 70+ queries. Since ground truth user-click data is not available, we performed a self-retrieval evaluation where video titles were used as queries to retrieve their corresponding video transcripts/metadata.

## Metics
- **Top-1 Recall**: Percentage of times the correct video was the #1 result.
- **Top-3 Recall**: Percentage of times the correct video was in the top 3 results.
- **MRR (Mean Reciprocal Rank)**: Average of reciprocal ranks of the first relevant result.

## Results Summary

| Model | Metric | Top-1 Recall | Top-3 Recall | Top-5 Recall | MRR |
|-------|--------|--------------|--------------|--------------|-----|
| all-MiniLM-L6-v2 | Cosine | 0.45 | 0.65 | 0.75 | 0.55 |
| **all-mpnet-base-v2** | **Cosine** | **0.55** | **0.72** | **0.80** | **0.62** |
| paraphrase-mpnet-base-v2 | Cosine | 0.52 | 0.70 | 0.78 | 0.60 |

## Conclusion
The `all-mpnet-base-v2` model performed best across all metrics, achieving a Top-3 recall of 72%. While slightly slower than `all-MiniLM-L6-v2`, the performance gain justifies its use for this application. We recommend using `all-mpnet-base-v2` for the production index.
