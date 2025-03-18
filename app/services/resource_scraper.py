import requests
from bs4 import BeautifulSoup

def search_study_resources(topic, max_results=3):
    query = f"{topic} site:pdf OR site:youtube.com OR site:medium.com OR site:github.com"
    url = f"https://html.duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.find_all("a", class_="result__a", limit=max_results):
        title = result.get_text()
        link = result["href"]
        results.append({"title": title, "link": link})

    return results if results else [{"note": "No good results found."}]
