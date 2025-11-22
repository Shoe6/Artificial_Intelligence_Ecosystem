# 3.1 Suppress Noisy Logs
import logging
import warnings

# Handle transformers logging safely
try:
    import transformers.logging as hf_logging
    hf_logging.set_verbosity_error()
except ImportError:
    pass

# Set logging levels to ERROR to avoid cluttering the console
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)

# Filter Python warnings
warnings.filterwarnings("ignore")

# 3.2 ChatGPT API Credentials
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# --- NEW: DEBUG CHECK ---
if not api_key:
    print("\n" + "="*50)
    print("CRITICAL ERROR: API Key NOT Found!")
    print("1. Check that your file is named '.env' (not .env.txt)")
    print("2. Make sure it contains: OPENAI_API_KEY=sk-proj-...")
    print("3. Ensure you SAVED the file (Ctrl+S)")
    print("="*50 + "\n")
    exit(1)
else:
    # Set the key for use
    openai.api_key = api_key

# 3.3 Parameters
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 20

# Re-ranking parameters
cross_encoder_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
top_m = 8

# 3.4 Read the Pre‑scraped Document
try:
    with open("Selected_Document.txt", "r", encoding="utf-8") as f:
        text = f.read()
    print(f"Successfully read 'Selected_Document.txt' ({len(text)} characters).")
except FileNotFoundError:
    print("Error: 'Selected_Document.txt' not found. Please run text_extractor.py first.")
    exit(1)

# 3.5 Split into Appropriately‑Sized Chunks
# Robust import for newer and older versions of LangChain
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', ' ', ''],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

chunks = text_splitter.split_text(text)
print(f"Split text into {len(chunks)} chunks.")

# 3.6 Embed & Build FAISS Index
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

print("Loading SentenceTransformer model...")
embedder = SentenceTransformer(model_name)

print("Encoding chunks...")
# Encode chunks and convert to float32 for FAISS
embeddings = embedder.encode(chunks, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Initialize FAISS index
dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings)
print(f"FAISS index built with {faiss_index.ntotal} vectors.")

# 3.7 Retrieval Function
def retrieve_chunks(question, k=top_k):
    """
    Retrieves the top k chunks similar to the question using the FAISS index.
    """
    # Encode the question
    q_vec = embedder.encode([question], show_progress_bar=False)
    q_arr = np.array(q_vec).astype("float32")
    
    # Search the index
    D, I = faiss_index.search(q_arr, k)
    
    # Retrieve corresponding text chunks
    # I[0] contains the indices of the neighbors for the first (and only) query vector
    retrieved_indices = I[0]
    return [chunks[i] for i in retrieved_indices]

# 3.8 Implement a Cross‑Encoder Re‑Ranker
from sentence_transformers import CrossEncoder

print("Loading CrossEncoder model...")
reranker = CrossEncoder(cross_encoder_name)

def dedupe_preserve_order(items):
    """
    Removes duplicates from a list while preserving the original order.
    Normalizes whitespace to catch near-duplicates.
    """
    seen = set()
    result = []
    for item in items:
        # Normalize whitespace for comparison
        normalized = " ".join(item.split())
        if normalized not in seen:
            seen.add(normalized)
            result.append(item)
    return result

def rerank_chunks(question: str, candidate_chunks: list[str], m: int = top_m) -> list[str]:
    """
    Re-ranks candidate chunks using a Cross-Encoder and returns the top m.
    """
    if not candidate_chunks:
        return []

    # Create pairs of (question, chunk) for the cross-encoder
    pairs = [[question, chunk] for chunk in candidate_chunks]
    
    # Score pairs
    scores = reranker.predict(pairs)
    
    # Sort by score descending (higher score = more relevant)
    # We zip chunks with scores, sort, and then unzip
    scored_chunks = sorted(zip(candidate_chunks, scores), key=lambda x: x[1], reverse=True)
    
    # Select top m chunks
    selected_chunks = [chunk for chunk, score in scored_chunks[:m]]
    
    # Light deduplication
    return dedupe_preserve_order(selected_chunks)

# 3.9 Q&A with ChatGPT
def answer_question(question):
    """
    Answers a user question using RAG (Retrieval Augmented Generation).
    1. Retrieves candidates via Bi-Encoder (FAISS).
    2. Re-ranks via Cross-Encoder.
    3. Generates answer via OpenAI API.
    """
    # 1. Retrieve
    candidates = retrieve_chunks(question, k=top_k)
    
    # 2. Re-rank
    relevant_chunks = rerank_chunks(question, candidates, m=top_m)
    
    # Join context
    context = "\n\n".join(relevant_chunks)
    
    # Define prompts
    system_prompt = (
        "You are a knowledgeable assistant that answers questions based on the provided context. "
        "If the answer is not in the context, say you don’t know."
    )
    
    user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""

    # 3. Call OpenAI API
    try:
        # Using standard OpenAI SDK structure
        from openai import OpenAI
        client = OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-4o", # Using gpt-4o as the latest stable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error generating answer: {e}"

# 3.10 Interactive Loop
if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("RAG App Initialized. Knowledge Base: Selected_Document.txt")
    print("Enter 'exit' or 'quit' to end.")
    print("------------------------------------------------------------")
    
    while True:
        question = input("\nYour question: ")
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        
        print("Thinking...")
        answer = answer_question(question)
        print("\nAnswer:", answer)