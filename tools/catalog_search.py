import requests
import streamlit as st

def catalog_search(query):
    api_key = st.secrets["CATALOG_API_KEY"]
    vid = st.secrets["CATALOG_PRIMO_VID"]

    url = "https://api-eu.hosted.exlibrisgroup.com/primo/v1/search"

    params = {
        "q": f"any,contains,{query}",
        "vid": vid,
        "limit": 3,
        "apikey": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return "Primo catalog API error."

    results = response.json()
    items = results.get("docs", [])
    
    if not items:
        return "No results found in catalog."

    output = []
    for item in items:
        title = item.get("pnx", {}).get("display", {}).get("title", ["No title"])[0]
        link = item.get("link", "")
        output.append(f"- [{title}]({link})")

    return "\n\n".join(output)
