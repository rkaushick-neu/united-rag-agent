from pdf_document import PDFDocument
from typing import List
from pathlib import Path
import argparse

class Parser:

    def parse_file(self, file_path: str):
        doc_file = Path(file_path)
        if not doc_file.is_file():
            raise ValueError("PARSER ERROR: Provided location is not a file!")

        document = None
        if file_path[-3:] == "pdf":
            document = PDFDocument(file_path)
        # more file types coming soon
        else:
            raise ValueError(f"Document of file type: {file_path[-3:]} is not supported yet.")

        print(f"Reading the document at location: {file_path} ...")
        document.extract_text()
        print(f"Extracted text from {document.name} file.")
        print(f"OPTIONAL: Saved the markdown file to ./docs/{document.name}.md")

    def parse_files(self, file_paths: List[str]):
        for file_path in file_paths:
            self.parse_file(file_path)
        pass   

# if the parser is executed separately:
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse a file")
    arg_parser.add_argument('--filepath', '-fp', help="The path of where the file is present in your local system")
    args = arg_parser.parse_args()
    # TODO: Fix up the argparse to handle multiple file paths
    parser = Parser()
    parser.parse_file(args.filepath)