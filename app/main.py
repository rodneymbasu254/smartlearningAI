from fastapi import FastAPI, Request, Form, UploadFile, File
from app.routes import upload
from app.services.study_plan_generator import generate_study_plan
from app.services.resource_scraper import search_study_resources
from app.services.quiz_generator import generate_quiz
from app.services.answer_evaluator import evaluate_answer
from app.services.research_assistant import gemini_topic_summary, scrape_web
from app.services.past_paper_analyzer import (
    extract_text_from_pdf, extract_text_from_docx,
    extract_questions, map_questions_to_topics,
    analyze_frequent_topics
)

app = FastAPI(title="SmartLearning AI")  # <-- This should appear before route definitions

# Optional: Dummy function for demo purposes
async def get_weekly_topics_from_db(unit):
    return [
        "Introduction to Topic",
        "Intermediate Concepts",
        "Advanced Theories"
    ]


@app.post("/analyze-past-paper")
async def analyze_past_paper(unit: str = Form(...), file: UploadFile = File(...)):
    weekly_topics = await get_weekly_topics_from_db(unit)

    file_text = ""
    if file.filename.endswith(".pdf"):
        file_text = extract_text_from_pdf(await file.read())
    elif file.filename.endswith(".docx"):
        file_text = extract_text_from_docx(file.file)
    else:
        return {"error": "Unsupported file format"}

    questions = extract_questions(file_text)
    mapped = map_questions_to_topics(questions, weekly_topics)
    frequency = analyze_frequent_topics(mapped)

    top_focus = list(frequency.keys())[:3]

    return {
        "unit": unit,
        "total_questions": len(questions),
        "most_frequent_topics": frequency,
        "focus_advice": f"For unit {unit}, focus more on: {', '.join(top_focus)}",
        "questions_mapped": mapped
    }


@app.post("/research/")
async def research(request: Request):
    body = await request.json()
    topic = body.get("topic")

    summary = gemini_topic_summary(topic)
    references = scrape_web(topic)

    return {
        "topic": topic,
        "summary": summary,
        "references": references
    }


@app.post("/weekly_quiz/")
async def weekly_quiz(request: Request):
    body = await request.json()
    topic = body.get("topic")
    quiz = generate_quiz(topic)
    return {"topic": topic, "quiz": quiz}


@app.post("/evaluate_answers/")
async def evaluate_answers(request: Request):
    body = await request.json()
    questions = body.get("questions", [])
    answers = body.get("answers", [])

    feedback = []
    total_score = 0

    for q, a in zip(questions, answers):
        result = evaluate_answer(q["question"], a)
        feedback.append({
            "question": q["question"],
            "student_answer": a,
            **result
        })
        total_score += result["score"]

    readiness = round((total_score / (len(questions) * 10)) * 100, 2)
    
    return {
        "readiness_score": readiness,
        "feedback": feedback
    }


@app.post("/generate_study_plan/")
async def get_study_plan(unit_data: dict):
    plan = generate_study_plan(unit_data)
    
    # Attach resources to each weekly topic
    for week in plan:
        topic = week["topic"]
        resources = search_study_resources(topic)
        week["resources"] = resources

    return {
        "status": "success",
        "study_plan": plan
    }


# Include router at the bottom
app.include_router(upload.router, prefix="/api")
