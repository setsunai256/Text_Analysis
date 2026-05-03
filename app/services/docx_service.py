from docx import Document
import tempfile


import os
from docx import Document
import tempfile


def extract_text_from_docx(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    try:
        doc = Document(tmp_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return text
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass