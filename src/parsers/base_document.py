from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Document(ABC):
    """Abstract base class for all document types (PDF, Word, Excel, etc.)."""
    
    def __init__(self, doc_id: str, metadata: Dict[str, Any]):
        self.doc_id = doc_id
        self.metadata = metadata
    
    @abstractmethod
    def extract_text(self) -> str:
        """Extract raw text (or Markdown) from the document."""
        pass

    @abstractmethod
    def to_chunks(self, max_tokens: int = 500) -> List[Dict[str, Any]]:
        """Split document into chunks with metadata for indexing."""
        pass
