import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_quiz(topic, num_questions=5):
    prompt = f"""
    Generate {num_questions} exam-style questions for university students on the topic: "{topic}".

    Return them in a valid JSON array format like:
    [
        {{ "question": "..." }},
        {{ "question": "..." }}
    ]
    """

    response = model.generate_content(prompt)

    try:
        # Extract JSON from the response (some responses include extra text/formatting)
        response_text = response.text.strip()
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        json_str = response_text[start:end]
        return json.loads(json_str)
    except Exception as e:
        return [{"question": f"Error generating questions: {str(e)}"}]
