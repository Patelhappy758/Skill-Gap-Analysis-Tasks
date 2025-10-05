import os
from typing import Tuple

from file_reader import read_txt
from file_reader_pdf import read_pdf
from file_reader_doc import read_docx
from text_cleaner import basic_clean

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def extract_text_auto(file_path: str) -> Tuple[str, str]:
    """
    Returns tuple of (raw_text, cleaned_text)
    """
    _, ext = os.path.splitext(file_path.lower())
    raw_text = ""
    if ext == ".txt":
        raw_text = read_txt(file_path)
    elif ext == ".pdf":
        raw_text = read_pdf(file_path)
    elif ext == ".docx":
        raw_text = read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    cleaned = basic_clean(raw_text)
    return raw_text, cleaned


