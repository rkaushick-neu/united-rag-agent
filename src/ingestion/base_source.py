from abc import ABC, abstractmethod
from typing import List
from parsers.base_document import Document

class Source(ABC):
    """Abstract base class for all sources (GoogleDrive, GoogleCloud, Outlook, etc.)."""

    @abstractmethod
    def fetch_documents(self) -> List[Document]:
        """Fetch documents from the source and return as Document objects."""
        pass