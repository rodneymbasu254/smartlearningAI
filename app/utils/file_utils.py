import fitz  # PyMuPDF
import docx
import pdfplumber

def extract_text_from_pdf(path):
    try:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(path):
    try:
        doc = docx.Document(path)
        full_text = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(full_text)
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
