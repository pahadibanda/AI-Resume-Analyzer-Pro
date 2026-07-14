"""Resume PDF text extractor using pdfplumber.

Shared utility `_extract_pdf_text` is imported by job_description_parser
to avoid code duplication.
"""
import pdfplumber


def _extract_pdf_text(pdf_path: str) -> str:
    """Extract and concatenate text from all pages of a PDF.

    Args:
        pdf_path: Absolute or relative path to the PDF file.

    Returns:
        Concatenated page text as a single string.
        Returns empty string if the file cannot be read.
    """
    text_parts: list[str] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception:
        return ""
    return "\n".join(text_parts)


def extract_text(pdf_path: str) -> str:
    """Extract text from a resume PDF file."""
    return _extract_pdf_text(pdf_path)