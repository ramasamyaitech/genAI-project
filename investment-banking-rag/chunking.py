import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DATA_PATH

def load_and_chunk_pdfs():
    """
    Loads PDFs from the data directory and splits them into chunks.
    Returns: List of Document objects.
    """
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Created directory: {DATA_PATH}. Please put your PDF files here.")
        return []

    print(f"Loading PDFs from {DATA_PATH}...")
    loader = DirectoryLoader(
        DATA_PATH, 
        glob="*.pdf", 
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    documents = loader.load()
    
    if not documents:
        print("No PDF documents found.")
        return []

    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)
    print(f"Generated {len(texts)} text chunks.")
    
    return texts