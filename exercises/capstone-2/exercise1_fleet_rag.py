import os
import faiss
import numpy as np
from litellm import completion, embedding
from dotenv import load_dotenv

load_dotenv()

# We will use OpenAI for embeddings and completions.
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-3.5-turbo"

def load_policy_data(filepath):
    """Loads and returns the text from the policy document."""
    # TODO: Read data/global_fleet_policy.md and return its contents
    pass

def chunk_text(text, chunk_size=300):
    """Splits text into smaller chunks."""
    # TODO: Implement a simple chunking strategy (e.g., split by paragraphs)
    return []

def embed_chunks(chunks):
    """Creates embeddings for each chunk using litellm."""
    # TODO: Call the embedding API and return a list of vectors
    return []

def build_faiss_index(embeddings):
    """Builds a FAISS vector index."""
    # TODO: Create a FAISS IndexFlatL2, add the embeddings, and return the index
    pass

def retrieve_context(query, index, chunks, k=2):
    """Embeds the query and retrieves the top-k chunks from FAISS."""
    # TODO: Embed the query, search the index, and return the matching chunks
    return ""

def answer_question(query, context):
    """Uses the LLM to answer the query based strictly on the context."""
    # TODO: Construct a prompt injecting the context and call the LLM
    pass

if __name__ == "__main__":
    # 1. Load and chunk data
    # 2. Embed chunks and build index
    # 3. Retrieve context for the query: "How often do I need an oil change?"
    # 4. Generate and print the answer
    print("Implement the TODOs to build your RAG system.")
