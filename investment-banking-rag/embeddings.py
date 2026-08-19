from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME, EMBEDDING_DEVICE

def get_embedding_model():
    """
    Initializes and returns the embedding model.
    """
    print(f"Loading Embedding Model: {EMBEDDING_MODEL_NAME}...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={'device': EMBEDDING_DEVICE},
        encode_kwargs={'normalize_embeddings': False}
    )
    return embeddings