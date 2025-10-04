from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Document(ABC):
    """Abstract base class for all document types (PDF, Word, Excel, etc.)."""
    
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
    
    @abstractmethod
    def extract_text(self) -> str:
        """Extract raw text (or Markdown) from the document."""
        pass