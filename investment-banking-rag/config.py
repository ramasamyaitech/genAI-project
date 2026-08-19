import os

# Paths
DATA_PATH = "data/"
DB_PATH = "stores/banking_cosine"

# Models
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en"
LLM_REPO = "TheBloke/neural-chat-7B-v3-1-GGUF"
EMBEDDING_DEVICE = 'cuda'

# Retrieval Config
RETRIEVER_K = 3

# LLM Config
LLM_CONFIG = {
    'context_length': 2048,
    'max_new_tokens': 1024,
    'repetition_penalty': 1.1,
    'temperature': 0.2,
    'top_k': 50,
    'top_p': 0.9,
    'stream': True,
    'gpu_layers': 0
}