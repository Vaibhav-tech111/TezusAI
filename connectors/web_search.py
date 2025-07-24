# connectors/web_search.py

import requests
from bs4 import BeautifulSoup

def search(query: str, num_results: int = 5) -> str:
    """
    Performs a basic web search using DuckDuckGo and returns top results.
    """

    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "TezusBot/1.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("a", class_="result__a")

    output = []
    for i, result in enumerate(results[:num_results]):
        title = result.text.strip()
        link = result.get("href")
        output.append(f"{i+1}. {title}\n🔗 {link}")

    return "\n".join(output) if output else "No results found."
