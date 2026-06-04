# Building with LLMs: Companion Resources

Companion repository for the book *Building with LLMs: The Developer's Handbook* by Kangeyan Passoubady.

This repo contains exercises, solutions, and large Excalidraw diagrams that complement the book.

## Structure

```
exercises/
  ch01/                      # Chapter 1: Introduction to Generative AI & LLMs
  ch03/                      # Chapter 3: Working with LLM APIs
  ch04/                      # Chapter 4: Model Capabilities & Limitations
  ch05/                      # Chapter 5: Prompt Engineering Fundamentals
  ch06/                      # Chapter 6: Prompting Techniques
  ch07/                      # Chapter 7: API Parameters & Output Control
  ch08/                      # Chapter 8: Prompt Iteration & Evaluation
  ch09/                      # Chapter 9: Conversation Design & Multi-turn Chat
  ch10/                      # Chapter 10: Embeddings & Vector Databases
  ch11/                      # Chapter 11: Retrieval-Augmented Generation (RAG)
  ch12/                      # Chapter 12: Security & Guardrails
  ch13/                      # Chapter 13: Cost, Latency & Error Handling
  ch14/                      # Chapter 14: Ethics, Bias & Evaluation
  capstone/                  # Capstone project (3 exercises)
solutions/
  ch01/ ... ch14/            # Reference solutions for each chapter
  capstone/                  # Capstone solutions
diagrams/
  ch01-transformer-full.excalidraw.png
  ch04-capability-matrix.excalidraw.png
  ...                        # Large Excalidraw diagrams (>6 elements)
shared/
  __init__.py
  llm_client.py              # Provider-agnostic LLM wrapper (litellm)
```

## Prerequisites

- Python 3.11+ (3.12 recommended)
- At least one LLM API key (OpenAI, Google Gemini, or Anthropic Claude)
- See the book's Appendix C for full setup instructions

## Quick Start

```bash
# Clone this repo
git clone https://github.com/kpassoubady/building-with-llms-companion.git
cd building-with-llms-companion

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure your API keys
cp .env.example .env
# Edit .env with your API keys

# Run an exercise
python exercises/ch01/tokenizer_explorer.py
```

## Exercise Format

Each exercise file contains:

- A docstring with the goal and skills practiced
- Starter code with `TODO` markers where you write your solution
- Hints in comments to guide you
- Expected output examples

Try each exercise before checking the reference solution in `solutions/`.

## Diagrams

The `diagrams/` folder contains large Excalidraw sketch diagrams (>6 visual elements) that
are referenced from book chapters but too large to inline. Each is named `chNN-description.excalidraw.png`.

## License

MIT

## Author

Kangeyan Passoubady (Kangs) | [Kavin School](https://kavinschool.com)
