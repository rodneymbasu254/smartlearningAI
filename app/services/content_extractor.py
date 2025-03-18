import re

def extract_course_content(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    course_code = extract_course_code(lines)
    course_title = extract_course_title(lines)
    objectives = extract_objectives(lines)
    weekly_topics = extract_weekly_topics(lines)
    study_materials = extract_study_materials(lines)
    
    return {
        "course_title": course_title,
        "course_code": course_code,
        "objectives": objectives,
        "weekly_topics": weekly_topics,
        "study_materials": study_materials
    }

def extract_course_code(lines):
    for line in lines[:10]:
        match = re.search(r"[A-Z]{2,4}\s*[-]?\s*\d{3}", line)
        if match:
            return match.group()
    return "Not Found"

def extract_course_title(lines):
    for line in lines[:10]:
        if any(keyword in line.lower() for keyword in ["course title", "unit title", "title:"]):
            return line.split(":")[-1].strip()
    # fallback
    return lines[0] if lines else "Untitled Course"

def extract_objectives(lines):
    objectives = []
    collecting = False
    for line in lines:
        if "objective" in line.lower():
            collecting = True
        elif collecting and (line.startswith("-") or line[0].isdigit()):
            objectives.append(line)
        elif collecting and line.strip() == "":
            break
    return objectives or ["Not Found"]

def extract_weekly_topics(lines):
    weekly_topics = []
    keywords = ["week", "topic", "outline"]
    collecting = False

    for line in lines:
        if any(k in line.lower() for k in keywords):
            collecting = True
        elif collecting and (line.startswith("-") or line[0].isdigit()):
            weekly_topics.append(line)
        elif collecting and re.match(r"^week\s*\d+", line.lower()):
            weekly_topics.append(line)
        elif collecting and line.strip() == "":
            break
    return weekly_topics or ["Not Found"]

def extract_study_materials(lines):
    materials = []
    collecting = False
    for line in lines:
        if "textbook" in line.lower() or "reference" in line.lower() or "reading" in line.lower():
            collecting = True
        elif collecting and (line.startswith("-") or line[0].isdigit()):
            materials.append(line)
        elif collecting and line.strip() == "":
            break
    return materials or ["Not Found"]
