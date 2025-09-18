# connectors/web_search.py

import requests
from bs4 import BeautifulSoup
import random
from lxml import html

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
]

def search(query: str, num_results: int = 5) -> str:
    """
    Performs a web search using DuckDuckGo and returns top results.  Includes error handling and improved parsing.
    """

    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": random.choice(user_agents)}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        tree = html.fromstring(response.content)
        results = tree.xpath("//div[@class='result__body']/a/@href")
        titles = tree.xpath("//div[@class='result__title']/a/text()")

        output = []
        for i in range(min(num_results, len(results))):
            title = titles[i].strip()
            link = results[i]
            output.append(f"{i+1}. {title}\n➡️ {link}")

        return "\n".join(output) if output else "No results found."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"