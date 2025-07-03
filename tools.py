# enhanced_library_bot/tools.py

from langchain.tools import tool
import urllib.parse
import streamlit as st
from tools.google_search import google_search

@tool
def search_primo(query: str) -> str:
    """Searches RCSI Bahrain Primo Catalog for a given keyword."""
    encoded = urllib.parse.quote(query)
    return f"[View Primo Results for '{query}'](https://rcsibahrain.primo.exlibrisgroup.com/discovery/search?query=any,contains,{encoded}&vid=973RCSIB_INST:RCSIB&lang=en)"

@tool
def search_libguides(query: str) -> str:
    """Searches the RCSI LibGuides site."""
    return f"[Search LibGuides for '{query}'](https://library.rcsi-mub.com/srch.php?query={urllib.parse.quote(query)})"

@tool
def search_google_scholar(query: str) -> str:
    """Searches Google Scholar for scholarly content."""
    return f"[Search Google Scholar for '{query}'](https://scholar.google.com/scholar?q={urllib.parse.quote(query)})"

@tool
def search_google(query: str) -> str:
    """Performs a Google search across library-specific or global content based on user selection."""
    mode = st.session_state.get("search_mode", "library")
    return google_search(query, mode)
