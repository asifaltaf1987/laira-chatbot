import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

@tool
def web_scrape_summary(query: str) -> str:
    """Scrapes and summarizes public websites related to a query."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        resp = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Try to extract first result link
        links = soup.select("a")
        first_result = next((a["href"] for a in links if "url?q=" in a["href"]), None)
        if not first_result:
            return "Couldn't find relevant webpages to scrape."

        # Clean and extract actual URL
        url = first_result.split("url?q=")[-1].split("&")[0]
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return f"Found info from: {url}\n\n{text[:1000]}..."  # Truncate long results
    except Exception as e:
        return f"Web scraping failed: {str(e)}"
