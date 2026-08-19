from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def load_pdf(file_path: str):

    print(f"Loading document: {file_path}")

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    print(f"Pages loaded: {len(documents)}")

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    return chunks


def process_pdf(file_path: str):

    documents = load_pdf(file_path)

    chunks = split_documents(documents)

    # Add useful metadata
    for chunk in chunks:

        chunk.metadata["source"] = Path(
            file_path
        ).name

    return chunks