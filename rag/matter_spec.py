# Processes Matter spec PDF files.
# Not used in current implementation as performance is not satisfactory

import os
import glob
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

COLLECTION_NAME = "matter-spec"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def prepare_documents_from_pdfs(matter_spec_dir):
    """Fetch and split PDF documents into chunks."""
    pdf_files = glob.glob(os.path.join(matter_spec_dir, "*.pdf"))
    all_text_data = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)

    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        chunks = text_splitter.split_text(text)

        # Store metadata with source info
        textData = [
            {"source": pdf_file, "text": chunk}
            for chunk in chunks
        ]
        all_text_data.extend(textData)

    print(f"✅ Successfully processed {len(all_text_data)} chunks from PDFs!")
    return all_text_data