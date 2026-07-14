"""Job Description PDF text extractor.

Reuses the shared `_extract_pdf_text` utility from resume_parser to avoid
code duplication. Both resume and JD parsing use identical pdfplumber logic.
"""
from modules.resume_parser import _extract_pdf_text


def extract_job_description(pdf_path: str) -> str:
    """Extract text from a Job Description PDF file."""
    return _extract_pdf_text(pdf_path)