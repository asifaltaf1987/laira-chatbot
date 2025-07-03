from scholarly import scholarly
from langchain.tools import tool

@tool
def scholar_search(query: str) -> str:
    """Searches Google Scholar and returns the first article title and author(s)."""
    try:
        search_result = next(scholarly.search_pubs(query), None)
        if search_result:
            title = search_result["bib"].get("title", "Untitled")
            author = search_result["bib"].get("author", "Unknown author(s)")
            return f"{title} — {author}"
        else:
            return "No scholarly articles found."
    except Exception as e:
        return f"Scholar search error: {str(e)}"
