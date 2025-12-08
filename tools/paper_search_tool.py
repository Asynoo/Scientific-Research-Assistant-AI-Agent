import requests
from typing import List, TypedDict


class ResearchPaper(TypedDict):
    title: str
    authors: List[str]
    year: int
    citation_count: int
    url: str


SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_papers(topic: str, year_filter: str = None, year: int = None,
                  end_year: int = None, min_citations: int = 0) -> List[ResearchPaper]:
    params = {
        "query": topic,
        "limit": 30,
        "fields": "title,authors,year,citationCount,url"
    }

    try:
        r = requests.get(SEMANTIC_SCHOLAR_SEARCH_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])
    except Exception:
        return []

    out = []
    for p in data:
        py = p.get("year")
        citations = p.get("citationCount", 0)

        if year_filter == "after" and (py is None or py <= year):
            continue
        elif year_filter == "range" and py is not None:
            if not (year <= py <= (end_year or 2024)):
                continue

        if min_citations > 0 and citations < min_citations:
            continue

        authors = [a.get("name", "") for a in p.get("authors", [])]

        out.append({
            "title": p.get("title", "Unknown"),
            "authors": authors,
            "year": py or 0,
            "citation_count": citations,
            "url": p.get("url", "")
        })

    return out