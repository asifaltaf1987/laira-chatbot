import requests
import streamlit as st

def google_search(query, mode="library"):
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # Choose CSE ID based on mode
    if mode == "global":
        cse_id = st.secrets["GOOGLE_CSE_ID_GLOBAL"]
    else:
        cse_id = st.secrets["GOOGLE_CSE_ID_LIBRARY"]

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": 3,
    }

    response = requests.get(url, params=params)
    results = response.json().get("items", [])

    if not results:
        return "No results found."

    return "\n\n".join([f"- [{r['title']}]({r['link']})" for r in results])
