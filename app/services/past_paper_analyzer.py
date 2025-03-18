import docx
import fitz  # PyMuPDF for PDFs
import re
from collections import defaultdict, Counter

# Extract text from .docx
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# Extract text from .pdf
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

# Extract questions using simple regex
def extract_questions(text):
    pattern = r"(?i)((Q[\d]+\.|Question\s[\d]+\.?)\s+.+)"
    questions = re.findall(pattern, text)
    return [q[0] for q in questions if q]

# Match questions to weekly topics
def map_questions_to_topics(questions, weekly_topics):
    topic_hits = defaultdict(list)
    for question in questions:
        for topic in weekly_topics:
            if topic.lower() in question.lower():
                topic_hits[topic].append(question)
    return dict(topic_hits)

# Frequency analysis
def analyze_frequent_topics(mapped_topics):
    freq = {topic: len(qs) for topic, qs in mapped_topics.items()}
    sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    return sorted_freq
