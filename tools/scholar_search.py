from scholarly import scholarly

def scholar_search(query):
    search_result = next(scholarly.search_pubs(query), None)
    if search_result:
        return f"{search_result['bib']['title']} — {search_result['bib'].get('author', '')}"
    return "No scholarly articles found."
