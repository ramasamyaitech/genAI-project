import hashlib
import json
from pathlib import Path
from typing import Any

from app.config import settings


class DocumentManager:

    def __init__(self):

        self.manifest_path = Path(
            settings.DOCUMENT_MANIFEST
        )

        self.manifest_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize_manifest()

    # --------------------------------------------------
    # Manifest
    # --------------------------------------------------

    def _initialize_manifest(self):

        if not self.manifest_path.exists():

            self.manifest_path.write_text(
                "[]",
                encoding="utf-8"
            )

    def _load_manifest(self) -> list[dict[str, Any]]:

        try:

            content = self.manifest_path.read_text(
                encoding="utf-8"
            )

            return json.loads(content)

        except (json.JSONDecodeError, OSError):

            return []

    def _save_manifest(
        self,
        documents: list[dict[str, Any]]
    ):

        self.manifest_path.write_text(
            json.dumps(
                documents,
                indent=4
            ),
            encoding="utf-8"
        )

    # --------------------------------------------------
    # Hash
    # --------------------------------------------------

    def calculate_hash(
        self,
        file_path: str
    ) -> str:

        sha256 = hashlib.sha256()

        with open(
            file_path,
            "rb"
        ) as file:

            for chunk in iter(
                lambda: file.read(8192),
                b""
            ):

                sha256.update(chunk)

        return sha256.hexdigest()

    # --------------------------------------------------
    # Duplicate detection
    # --------------------------------------------------

    def document_exists(
        self,
        document_hash: str
    ) -> bool:

        documents = self._load_manifest()

        return any(
            document["document_hash"] == document_hash
            for document in documents
        )

    # --------------------------------------------------
    # Register
    # --------------------------------------------------

    def register_document(
        self,
        filename: str,
        document_hash: str,
        chunks: int,
        size_bytes: int
    ):

        documents = self._load_manifest()

        documents.append(
            {
                "filename": filename,
                "document_hash": document_hash,
                "chunks": chunks,
                "size_bytes": size_bytes
            }
        )

        self._save_manifest(
            documents
        )

    # --------------------------------------------------
    # List
    # --------------------------------------------------

    def list_documents(self):

        return self._load_manifest()

    # --------------------------------------------------
    # Delete metadata
    # --------------------------------------------------

    def remove_document_metadata(
        self,
        filename: str
    ):

        documents = self._load_manifest()

        documents = [
            document
            for document in documents
            if document["filename"] != filename
        ]

        self._save_manifest(
            documents
        )


document_manager = DocumentManager()