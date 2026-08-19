from config import RETRIEVER_K

def get_retriever(vector_store):
    """
    Converts the vector store into a retriever object.
    
    Args:
        vector_store: The ChromaDB instance.
    
    Returns:
        A LangChain retriever object.
    """
    print(f"Initializing Retriever with k={RETRIEVER_K}...")
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={'k': RETRIEVER_K}
    )
    return retriever