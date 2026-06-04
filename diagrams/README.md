# Excalidraw Diagrams (Large, >6 Elements)

These hand-drawn sketch diagrams complement the book chapters. They are too large
(>6 visual elements) to inline in the book, so they live here in the companion repo.

Each diagram is referenced from its respective book chapter with a note like:
"See the companion repo for the full diagram."

## Diagram Inventory

| File | Chapter | Elements | Description |
|:-----|:--------|:---------|:------------|
| `ch01-transformer-full.excalidraw.png` | Ch 1 | ~12 | Complete Transformer architecture: input embedding, positional encoding, multi-head attention (Q/K/V), add & norm, feed-forward, output probabilities |
| `ch04-capability-matrix.excalidraw.png` | Ch 4 | ~15 | Full capability matrix: 10 tasks x reliability rating + best model + cost tier, color-coded cells |
| `ch06-technique-matrix.excalidraw.png` | Ch 6 | ~10 | Technique comparison: 6 techniques x when to use, pros, cons, example task |
| `ch08-eval-pipeline.excalidraw.png` | Ch 8 | ~10 | Complete evaluation pipeline: Golden Dataset to Prompt Runner to Scorer to Report Generator |
| `ch10-chunking-indexing.excalidraw.png` | Ch 10 | ~9 | Full chunking and indexing pipeline: Document to Loader to Splitter to Embedding to Vector DB |
| `ch11-rag-full.excalidraw.png` | Ch 11 | ~12 | Complete RAG architecture: ingestion pipeline + query pipeline + evaluation feedback loops |
| `ch13-cost-decision-tree.excalidraw.png` | Ch 13 | ~10 | Cost optimization decision tree with estimated savings percentages at each leaf |
| `ch14-eval-harness.excalidraw.png` | Ch 14 | ~12 | Complete evaluation harness: Golden Dataset to Multi-Scorer to Drift Monitor to Alert System |

## Style Guidelines

All diagrams use:
- Excalidraw hand-drawn/sketch style (default)
- Color coding: green = good/success, red = bad/fail, blue = neutral/info
- Clear labels on every element
- Left-to-right or top-to-bottom flow direction
