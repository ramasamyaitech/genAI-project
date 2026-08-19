from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

from config import logger


class WebsiteLoader:

    def load(self, url: str) -> list[Document]:

        logger.info(f"Loading Website: {url}")

        loader = WebBaseLoader(url)

        documents = loader.load()

        logger.info(f"Loaded {len(documents)} web document(s)")

        return documents