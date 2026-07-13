import os

try:
    import fitz
except ImportError:
    fitz = None


def process_pdf(pdf_path: str) -> dict:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed")

    doc = fitz.open(pdf_path)
    pages_text = []
    tables = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages_text.append(text)

    markdown_content = "\n\n".join(pages_text)

    metadata = {
        "filename": os.path.basename(pdf_path),
        "pages": len(doc),
    }

    doc.close()

    return {
        "markdown": markdown_content,
        "tables": tables,
        "metadata": metadata,
    }
