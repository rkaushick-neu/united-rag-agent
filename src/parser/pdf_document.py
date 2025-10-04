# import requests
# import re
import os
# import json
from dotenv import load_dotenv
from typing import List, Dict, Any
from pathlib import Path
from mistralai import Mistral, DocumentURLChunk
from base_document import Document

class PDFDocument(Document):
    def __init__(self, file_path: str):
        doc_file = Path(file_path)
        self.type = "pdf"
        self.bytes = doc_file.read_bytes()
        self.text = None # this will include the markdown text
        # doc_file.stem: removes the leading folders & the name of the extension
        super().__init__(name=doc_file.stem, type=self.type)

    @staticmethod
    def _replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
        """
        Replace image placeholders in markdown with base64-encoded images.

        Args:
            markdown_str: Markdown text containing image placeholders
            images_dict: Dictionary mapping image IDs to base64 strings

        Returns:
            Markdown text with images replaced by base64 data
        """
        for img_name, base64_str in images_dict.items():
            markdown_str = markdown_str.replace(
                f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
            )
        return markdown_str

    @staticmethod
    def _get_combined_markdown(ocr_response) -> str:
        """
        Combine OCR text and images into a single markdown document.

        Args:
            ocr_response: Response from OCR processing containing text and images

        Returns:
            Combined markdown string with embedded images
        """
        markdowns: list[str] = []
        # Extract images from page
        for page in ocr_response.pages:
            image_data = {}
            for img in page.images:
                image_data[img.id] = img.image_base64
            # Replace image placeholders with actual images
            markdowns.append(PDFDocument._replace_images_in_markdown(page.markdown, image_data))

        return "\n\n".join(markdowns)

    def _ocr_to_markdown(self) -> str:
        """
        Send PDF bytes to Mistral OCR API, get structured Markdown output.
        
        Args:
            file_data: raw bytes of the PDF document.
        
        Returns:
            markdown_text: the OCR output in Markdown format.
        """

        # Load Mistral configuration
        load_dotenv()
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        
        if not mistral_api_key:
            raise RuntimeError("Missing MISTRAL_API_KEY in the environment variables (.env file)") 

        # Initialize Mistral client
        client = Mistral(api_key=mistral_api_key)
        
        # Upload PDF file to Mistral
        uploaded_file = client.files.upload(
            file={
                "file_name": self.name,
                "content": self.bytes,
            },
            purpose="ocr",
        )
        
        # Get signed URL for the uploaded file
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
        
        # Process PDF with OCR, including embedded images
        pdf_response = client.ocr.process(
            document=DocumentURLChunk(document_url=signed_url.url),
            model="mistral-ocr-latest",
            include_image_base64=True
        )
        
        # Combine markdown and images into final output
        markdown_text = PDFDocument._get_combined_markdown(pdf_response)        
        return markdown_text

    def _save_markdown_to_file(self, file_path: str) -> None:
        """
        Save the markdown output to a local file for debugging or later use.

        Args:
            file_path: The file path where the markdown will be saved.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.text)

    def extract_text(self) -> None:
        """Download PDF, run OCR, and return Markdown text."""
        
        # Send file_data to Mistral OCR API
        markdown_text = self._ocr_to_markdown()
        self.text = markdown_text
        # optionally save the markdown to the local system
        self._save_markdown_to_file(file_path=f"./docs/{self.name}.md")

    def _load_markdown_from_file(self, file_path: str) -> None:
        """
        Load the markdown from a local file back into the object. 
        This method is written to test out the chunking without having to run the ocr to markdown each time. 

        Args:
            file_path: The file path where the markdown is stored.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            self.text = f.read()

if __name__ == "__main__":    
    file_path = "/Users/rishabhkaushick/Documents/Northeastern/CSYE7230/Papers/Billion-scale similarity search with GPUs.pdf"
    print(f"Reading the PDF at file_path: {file_path} ...")
    pdf_document = PDFDocument(file_path=file_path)
    pdf_document.extract_text()
    print(f"Extracted text from {pdf_document.name} PDF file.")
    print(f"OPTIONAL: Saved the markdown file to ./docs/{pdf_document.name}.md")