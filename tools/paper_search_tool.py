from typing import List, TypedDict

import requests


class ResearchPaper(TypedDict):
    title: str
    authors: List[str]
    year: int
    citation_count: int
    url: str


SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_papers(topic: str, year_filter: str = None, year: int = None, citation_filter: str = None,
                  citation_count: int = 0) -> List[ResearchPaper]:
    params = {
        "query": topic,
        "limit": 20,
        "fields": "title,authors,year,citationCount,url"
    }

    try:
        resp = requests.get(SEMANTIC_SCHOLAR_SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
    except Exception:
        return []

    filtered = []
    for p in data:
        try:
            py = p.get("year")
            pc = p.get("citationCount", 0)

            if year_filter == "in" and py != year:
                continue
            if year_filter == "before" and (py is not None and py >= year):
                continue
            if year_filter == "after" and (py is not None and py <= year):
                continue

            if citation_filter == "exactly" and pc != citation_count:
                continue
            if citation_filter == "at least" and pc < citation_count:
                continue
            if citation_filter == "at most" and pc > citation_count:
                continue

            authors = [a.get("name", "") for a in p.get("authors", [])]

            filtered.append({
                "title": p.get("title", "Unknown"),
                "authors": authors,
                "year": py or 0,
                "citation_count": pc,
                "url": p.get("url", "")
            })
        except Exception:
            continue

    return filtered
