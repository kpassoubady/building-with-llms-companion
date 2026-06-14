import os
import faiss
import numpy as np
from litellm import completion, embedding
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-3.5-turbo"

def load_policy_data(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def chunk_text(text, chunk_size=300):
    # Simple split by double newline (paragraphs)
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

def embed_chunks(chunks):
    response = embedding(model=EMBEDDING_MODEL, input=chunks)
    return [item['embedding'] for item in response.data]

def build_faiss_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    # FAISS expects numpy arrays of type float32
    vectors = np.array(embeddings).astype('float32')
    index.add(vectors)
    return index

def retrieve_context(query, index, chunks, k=2):
    query_emb = embedding(model=EMBEDDING_MODEL, input=[query]).data[0]['embedding']
    query_vec = np.array([query_emb]).astype('float32')
    distances, indices = index.search(query_vec, k)
    
    # Retrieve the corresponding text chunks
    retrieved_chunks = [chunks[i] for i in indices[0]]
    return "\n\n".join(retrieved_chunks)

def answer_question(query, context):
    messages = [
        {"role": "system", "content": "You are a Global Fleet assistant. Answer questions strictly based on the provided policy context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
    response = completion(model=LLM_MODEL, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Loading data...")
    # Adjust path if running from root
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "global_fleet_policy.md")
    if not os.path.exists(data_path):
        data_path = "data/global_fleet_policy.md"
        
    policy_text = load_policy_data(data_path)
    
    print("Chunking and embedding...")
    chunks = chunk_text(policy_text)
    embeddings = embed_chunks(chunks)
    
    print("Building index...")
    index = build_faiss_index(embeddings)
    
    query = "How often do I need an oil change?"
    print(f"\nQuery: {query}")
    
    context = retrieve_context(query, index, chunks, k=2)
    print("\n--- Retrieved Context ---")
    print(context)
    
    answer = answer_question(query, context)
    print("\n--- Answer ---")
    print(answer)
