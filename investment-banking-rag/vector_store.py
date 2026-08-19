import os
from langchain_chroma import Chroma
from config import DB_PATH

def create_vector_db(texts, embeddings):
    """
    Creates a new vector store from text chunks and saves it.
    """
    if not texts:
        print("No texts to process.")
        return

    print(f"Creating and persisting Vector Store to {DB_PATH}...")
    vectorstore = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_metadata={'hnsw:space': 'cosine'}
    )
    print("Vector Store created successfully.")

def load_vector_db(embeddings):
    """
    Loads an existing vector store.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database path '{DB_PATH}' does not exist. Run ingest.py first.")

    print(f"Loading Vector Store from {DB_PATH}...")
    return Chroma(
        persist_directory=DB_PATH, 
        embedding_function=embeddings
    )