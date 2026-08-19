from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


def load_pdf(file_path: str):

    print(f"Loading document: {file_path}")

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    print(
        f"Pages loaded: {len(documents)}"
    )

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

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    return chunks


def process_pdf(file_path: str):

    documents = load_pdf(file_path)

    if not documents:

        raise ValueError(
            "No pages could be extracted from PDF."
        )

    chunks = split_documents(
        documents
    )

    if not chunks:

        raise ValueError(
            "No text chunks could be created from PDF."
        )

    filename = Path(file_path).name

    for index, chunk in enumerate(chunks):

        chunk.metadata["source"] = filename

        chunk.metadata["chunk_id"] = index

        if "page" in chunk.metadata:

            chunk.metadata["page_number"] = (
                chunk.metadata["page"] + 1
            )

    return chunks