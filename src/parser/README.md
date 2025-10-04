# Parser Module

The **Parser** module is responsible for extracting and converting the content of documents into a structured markdown format. Currently, it supports parsing PDF files, with plans to extend support to Excel and Word documents in the near future. This module serves as the first step in the overall pipeline.

## Overview
- **Input:** A document file (currently PDF).
- **Output:** A markdown (`.md`) file containing the parsed content (stored in the `/docs` folder)
- **Purpose:** To transform raw document data into a clean, structured markdown format that can be easily processed in subsequent steps such as chunking and embedding.

## Running the Parser Independently

If you want to run only the parsing step without executing the entire pipeline, you can use the command line interface provided by the parser script.

### Command-Line Usage

```bash
python src/parser/parser.py --filepath '/absolute/path/to/document.pdf'
```

or using the shorthand flag: 

```bash
python src/parser/parser.py -fp '/absolute/path/to/document.pdf'
```

### Example

```bash
python src/parser/parser.py --filepath '/Users/xyz/Documents/Papers/Attention Is All You Need.pdf'
```

This command will parse the specified PDF file and output a markdown file containing the extracted content in markdown format. The output is stored in the `/docs` folder.

## Expected Output

- A markdown file containing the text extracted from the PDF.
- The markdown preserves the structure of the original document as much as possible, such as headings, paragraphs, and lists.