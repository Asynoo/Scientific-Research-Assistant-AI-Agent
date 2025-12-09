def use_case_1():
    return """Find papers on "large language models":
- Published after 2020
- At least 20 citations
- Include: title, authors, year, citation_count, url
- At least 2 papers
- JSON format: {"papers": [{"title": "...", "authors": ["..."], "year": ..., "citation_count": ..., "url": "..."}], "summary": "..."}
Only JSON."""

def use_case_2():
    return """Find papers on "climate adaptation":
- Published after 2020  
- At least 10 citations
- Include: title, authors, year, citation_count, url
- At least 2 papers
- JSON format: {"papers": [{"title": "...", "authors": ["..."], "year": ..., "citation_count": ..., "url": "..."}], "summary": "..."}
Only JSON."""

def use_case_3():
    return """Find papers on "AI diagnosis":
- Published after 2019
- At least 20 citations
- Include: title, authors, year, citation_count, url
- At least 2 papers
- JSON format: {"papers": [{"title": "...", "authors": ["..."], "year": ..., "citation_count": ..., "url": "..."}], "summary": "..."}
Only JSON."""