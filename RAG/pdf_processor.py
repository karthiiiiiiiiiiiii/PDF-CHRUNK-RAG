import fitz

from chunker import chunk_text
from embeddings import create_embeddings
from retriever import create_faiss_index


def extract_text_from_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_num, page in enumerate(doc):

        text = page.get_text("text").strip()

        if text:

            pages.append(
                {
                    "page": page_num + 1,
                    "text": text
                }
            )

    doc.close()

    return pages


def process_pdf(pdf_path):

    # Extract text
    pages = extract_text_from_pdf(pdf_path)

    # Create semantic chunks
    chunks = chunk_text(pages)

    # Generate embeddings
    embeddings = create_embeddings(chunks)

    # Create FAISS index
    index = create_faiss_index(embeddings)

    return index, chunks