import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def evaluate_answer(question, student_answer):
    prompt = f"""
    Evaluate the student's answer.

    Question: {question}
    Student Answer: {student_answer}

    - Score (0 to 10)
    - Correctness (True/False)
    - Feedback (Explain why correct/incorrect)
    - Confidence (Low, Medium, High)

    Return in JSON format like:
    {{
      "score": 7,
      "correct": true,
      "feedback": "Good answer but missed example",
      "confidence": "Medium"
    }}
    """

    response = model.generate_content(prompt)
    
    # Gemini responses often include markdown — we'll extract just the JSON part
    try:
        # Find the JSON block in the response text
        response_text = response.text.strip()
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        json_str = response_text[start:end]
        return json.loads(json_str)
    except Exception as e:
        return {
            "score": 0,
            "correct": False,
            "feedback": f"Failed to evaluate answer: {str(e)}",
            "confidence": "Low"
        }
