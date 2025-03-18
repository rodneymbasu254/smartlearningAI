from app.utils.file_utils import extract_text_from_pdf, extract_text_from_docx
from app.services.content_extractor import extract_course_content

def extract_course_info(path, ext):
    if ext == "pdf":
        text = extract_text_from_pdf(path)
    elif ext == "docx":
        text = extract_text_from_docx(path)
    
    # Extract core content from text
    course_data = extract_course_content(text)
    return course_data
