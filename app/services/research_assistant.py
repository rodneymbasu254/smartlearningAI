import os
import json
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv

# Load your Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 1: Use Gemini to understand topic
def gemini_topic_summary(topic):
    prompt = f"""
    Summarize and explain the topic: "{topic}" for a university student.

    Include:
    - Brief summary
    - Key subtopics
    - Suggested books (if any)
    - Real-world applications
    - Suggested follow-up study topics

    Format the response as markdown-styled dictionary like:
    {{
      "summary": "...",
      "subtopics": ["...", "..."],
      "books": ["...", "..."],
      "applications": ["...", "..."],
      "follow_up": ["...", "..."]
    }}
    """

    response = model.generate_content(prompt)
    try:
        # Extract JSON content from Gemini's output
        text = response.text.strip()
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception as e:
        return {"error": f"Failed to parse Gemini response: {str(e)}"}

# Step 2: Web scrape resources from .edu
def scrape_web(topic):
    try:
        query = topic.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}+site:edu"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "http" in href and "edu" in href:
                match = re.search(r"(https?://[^\s]+)", href)
                if match:
                    links.append(match.group(1))

        return list(set(links))[:5]  # Top 5 .edu references
    except Exception as e:
        return [f"Error during scraping: {str(e)}"]
