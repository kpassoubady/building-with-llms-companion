# Building with LLMs: Companion Repository

Hands-on exercises, solutions, and capstone projects for the "Building with LLMs" book. Each chapter (1-14) has 2-3 exercises with TODO scaffolding, plus two capstone projects that integrate skills across multiple chapters.

## Related repositories

| Repo | Path | Purpose |
| :--- | :--- | :--- |
| building-with-llms-book | `../building-with-llms-book` | Book manuscript (chapters, diagrams, build system) |
| gen-ai | `../gen-ai` | Instructor-led 4-day course (slides, labs, demos) |
| gen-ai-setup | `../gen-ai-setup` | Pre-class setup, install guides, environment verification |

## Repository structure

```
building-with-llms-companion/
  exercises/
    ch01/ through ch14/        Chapter exercises (2-3 per chapter)
    capstone-1/                Global Fleet Intelligence (Chapters 1-8 skills)
    capstone-2/                Global Intelligent Fleet Assistant (Chapters 9-14 skills)

  solutions/
    ch01/ through ch14/        Reference solutions (mirrors exercises/)

  shared/
    __init__.py                Exports: get_completion, get_completion_full, etc.
    llm_client.py              Provider-agnostic LLM wrapper (litellm)

  diagrams/                    Excalidraw diagrams (.excalidraw, .json, .png)
  assets/                      Brand assets (logos, theme CSS)
  references/                  Reference docs (model-naming-guide.md)

  .env.example                 API key configuration template
  requirements.txt             Python dependencies
  package.json                 Node.js dependencies (Playwright)
```

## Tech stack

- Python 3.11+ (3.12 recommended)
- litellm for provider-agnostic LLM routing
- Providers: OpenAI (GPT-4o), Gemini (2.5 Flash), Claude (Sonnet 4)
- Vector databases: faiss-cpu, chromadb
- Web frameworks: Flask, FastAPI + uvicorn
- Tokenization: tiktoken
- Browser automation: Playwright (Node.js)

## Shared LLM client

All exercises use the provider-agnostic wrapper in `shared/llm_client.py`:

```python
from shared import get_completion, get_completion_full, get_embedding, show_config

# Simple call (returns string)
response = get_completion(
    messages=[{"role": "user", "content": "Hello"}],
    tier="mini",        # "mini" = fast/cheap, "default" = capable
    temperature=0.7,
)

# Full response (returns litellm response object)
response = get_completion_full(messages=[...], tier="default")

# Embeddings (OpenAI or Gemini only, Claude has no embeddings API)
vectors = get_embedding(["text1", "text2"])
```

Provider priority is set via `.env`:
```
LLM_PROVIDER_PRIORITY=gemini,openai,claude    # fallback chain
LLM_PROVIDER=openai                           # force single provider (optional)
```

## Exercise file conventions

**File naming:** Descriptive snake_case: `tokenizer_explorer.py`, `rag_pipeline.py`

**Standard header:**
```python
"""
Exercise: Name
Chapter N: Chapter Title

Goal: One sentence.

Skills practiced:
- Skill 1
- Skill 2

Instructions:
1. Step 1
2. Step 2

Run: python exercises/chNN/filename.py  (from repo root)
"""
```

**Code structure:**
- Path insertion: `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))`
- Import from shared: `from shared import get_completion, show_config`
- Sample data as module-level constants
- Functions with `TODO` markers and hints in comments
- `main()` function that orchestrates the exercise
- `if __name__ == "__main__": main()`
- Expected output examples in trailing comments

**Solution files:** Mirror the exercise directory structure under `solutions/chNN/`. Fully working, no TODOs.

## Capstone projects

**Capstone 1: Global Fleet Intelligence** (exercises/capstone-1/)
- Exercise 1: Driver Issue Classifier (role prompting, structured JSON)
- Exercise 2: Work Order Parser (few-shot, CoT, cost estimation)
- Exercise 3: Fleet Service Advisor (golden dataset, LLM-as-judge, prompt versioning)
- Solutions in `capstone-1/solutions/`
- Slides in `capstone-1/slides/`

**Capstone 2: Global Intelligent Fleet Assistant** (exercises/capstone-2/)
- Exercise 1: Fleet Policy RAG System (chunking, embedding, retrieval)
- Exercise 2: Guardrailed Maintenance Chatbot (multi-turn, input/output guardrails)
- Exercise 3: Maintenance Invoice Evaluator (evaluation harness, accuracy metrics)
- Solutions in `capstone-2/solutions/`
- Data files in `capstone-2/data/` (global_fleet_policy.md, invoice_dataset.json)
- Slides in `capstone-2/slides/`

## Diagrams

Large Excalidraw diagrams (>6 visual elements) live in `diagrams/`. Each diagram has three files:
- `.excalidraw` - editable source
- `.json` - JSON export
- `.png` - PNG export for viewing

Style: hand-drawn/sketch style, color-coded (green = good, red = bad, blue = neutral), clear labels, left-to-right or top-to-bottom flow.

## Writing style

Same rules as the book and course repos:
- No em dash or en dash. Plain hyphen is fine.
- No antithesis patterns, hedging filler, hype words, or LLM openers.
- Bold only in headings, table headers, and definition-style list terms.

## Common tasks

- Add a new exercise: create file in `exercises/chNN/` with the standard header, add corresponding solution in `solutions/chNN/`, update `exercises/chNN/README.md`.
- Add a diagram: create in Excalidraw, export as `.excalidraw`, `.json`, `.png`, name as `chNN-description.*`, add to `diagrams/README.md`.
- Add a Python package: add to `requirements.txt` with a minimum version pin.
- Update provider models: edit `PROVIDER_MODELS` in `shared/llm_client.py`.
- Run an exercise: `python exercises/chNN/filename.py` from the repo root.

## Linting

Markdown linting configured via `.markdownlint.json` (most rules disabled). Enabled rules: MD001 (heading levels), MD047 (trailing newline).
