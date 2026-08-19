import threading
from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.config import settings
from app.document_manager import document_manager
from app.document_processor import process_pdf
from app.embeddings import get_embedding_model
from app.ollama_service import get_llm
from app.prompts import RAG_PROMPT


class RAGService:

    def __init__(self):

        self.embedding_model = (
            get_embedding_model()
        )

        self.llm = get_llm()

        self.vectorstore = None

        # Prevent simultaneous FAISS writes
        self.index_lock = threading.Lock()

        self.load_vectorstore()

    # ==================================================
    # Vectorstore
    # ==================================================

    def load_vectorstore(self):

        index_path = Path(
            settings.VECTOR_DB_PATH
        )

        index_file = (
            index_path / "index.faiss"
        )

        if not index_file.exists():

            print(
                "FAISS vectorstore does not exist yet."
            )

            return

        try:

            print(
                "Loading existing FAISS vectorstore..."
            )

            self.vectorstore = FAISS.load_local(
                str(index_path),
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

            print(
                "FAISS vectorstore loaded successfully."
            )

        except Exception as exc:

            print(
                f"Failed to load FAISS vectorstore: {exc}"
            )

            self.vectorstore = None

    # ==================================================
    # Add document
    # ==================================================

    def add_document(
        self,
        file_path: str
    ):

        file_path_obj = Path(
            file_path
        )

        if not file_path_obj.exists():

            raise FileNotFoundError(
                "PDF file does not exist."
            )

        document_hash = (
            document_manager.calculate_hash(
                file_path
            )
        )

        # --------------------------------------------------
        # Duplicate check
        # --------------------------------------------------

        if document_manager.document_exists(
            document_hash
        ):

            raise ValueError(
                "This document has already been indexed."
            )

        # --------------------------------------------------
        # Process PDF
        # --------------------------------------------------

        chunks = process_pdf(
            file_path
        )

        if not chunks:

            raise ValueError(
                "No usable text was extracted from PDF."
            )

        # --------------------------------------------------
        # FAISS write lock
        # --------------------------------------------------

        with self.index_lock:

            if self.vectorstore is None:

                print(
                    "Creating new FAISS vectorstore..."
                )

                self.vectorstore = (
                    FAISS.from_documents(
                        chunks,
                        self.embedding_model
                    )
                )

            else:

                print(
                    "Adding chunks to existing FAISS..."
                )

                self.vectorstore.add_documents(
                    chunks
                )

            # --------------------------------------------------
            # Persist
            # --------------------------------------------------

            vector_path = Path(
                settings.VECTOR_DB_PATH
            )

            vector_path.mkdir(
                parents=True,
                exist_ok=True
            )

            self.vectorstore.save_local(
                str(vector_path)
            )

        # --------------------------------------------------
        # Register document
        # --------------------------------------------------

        document_manager.register_document(
            filename=file_path_obj.name,
            document_hash=document_hash,
            chunks=len(chunks),
            size_bytes=file_path_obj.stat().st_size
        )

        return {
            "chunks": len(chunks),
            "document_hash": document_hash
        }

    # ==================================================
    # Retrieval
    # ==================================================

    def retrieve_documents(
        self,
        question: str
    ):

        if self.vectorstore is None:

            raise ValueError(
                "Vector database is empty. "
                "Please upload a PDF first."
            )

        results = (
            self.vectorstore
            .similarity_search_with_score(
                question,
                k=settings.TOP_K
            )
        )

        filtered_documents = []

        for document, score in results:

            print(
                f"Retrieved: "
                f"{document.metadata.get('source')} "
                f"| page={document.metadata.get('page_number')} "
                f"| score={score:.4f}"
            )

            # FAISS L2 distance:
            # lower score = better similarity

            if score <= settings.SIMILARITY_THRESHOLD:

                filtered_documents.append(
                    document
                )

        return filtered_documents

    # ==================================================
    # Build context
    # ==================================================

    def build_context(
        self,
        documents
    ):

        context_parts = []

        sources = set()

        for index, document in enumerate(
            documents,
            start=1
        ):

            content = (
                document.page_content.strip()
            )

            source = document.metadata.get(
                "source",
                "Unknown"
            )

            page = document.metadata.get(
                "page_number"
            )

            if page is not None:

                source_name = (
                    f"{source} - Page {page}"
                )

            else:

                source_name = source

            sources.add(
                source_name
            )

            context_parts.append(
                f"--- DOCUMENT {index} ---\n"
                f"Source: {source_name}\n\n"
                f"{content}"
            )

        context = "\n\n".join(
            context_parts
        )

        return context, sorted(sources)

    # ==================================================
    # Ask question
    # ==================================================

    def ask_question(
        self,
        question: str
    ):

        question = question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        documents = (
            self.retrieve_documents(
                question
            )
        )

        # --------------------------------------------------
        # No relevant documents
        # --------------------------------------------------

        if not documents:

            return {
                "answer": (
                    "The information is not available "
                    "in the provided documents."
                ),
                "sources": []
            }

        # --------------------------------------------------
        # Context
        # --------------------------------------------------

        context, sources = (
            self.build_context(
                documents
            )
        )

        # --------------------------------------------------
        # Prompt
        # --------------------------------------------------

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        # --------------------------------------------------
        # LLM
        # --------------------------------------------------

        answer = self.llm.invoke(
            prompt
        )

        if not answer:

            answer = (
                "The information is not available "
                "in the provided documents."
            )

        return {
            "answer": str(answer).strip(),
            "sources": sources
        }


rag_service = RAGService()