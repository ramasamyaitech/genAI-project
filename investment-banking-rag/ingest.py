from chunking import load_and_chunk_pdfs
from embeddings import get_embedding_model
from vector_store import create_vector_db

def main():
    # 1. Load and Chunk
    texts = load_and_chunk_pdfs()
    
    # 2. Initialize Embeddings
    embedding_model = get_embedding_model()
    
    # 3. Create Vector Store
    create_vector_db(texts, embedding_model)

if __name__ == "__main__":
    main()