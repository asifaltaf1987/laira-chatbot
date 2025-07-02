from langchain.tools import tool
import urllib.parse

@tool
def search_primo(query: str) -> str:
    """Searches RCSI Bahrain Primo Catalog for a given keyword."""
    encoded = urllib.parse.quote(query)
    return f"[View Primo Results for '{query}'](https://rcsibahrain.primo.exlibrisgroup.com/discovery/search?query=any,contains,{encoded}&vid=973RCSIB_INST:RCSIB&lang=en)"

@tool
def search_google_scholar(query: str) -> str:
    """Simulate a Google Scholar search."""
    return f"[Search Google Scholar for '{query}'](https://scholar.google.com/scholar?q={urllib.parse.quote(query)})"

@tool
def search_libguides(query: str) -> str:
    """Search the RCSI LibGuides site."""
    return f"[Search LibGuides for '{query}'](https://library.rcsi-mub.com/srch.php?query={urllib.parse.quote(query)})"