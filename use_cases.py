def use_case_1():
    return """
    Find research papers on "machine learning transformers" with constraints:
    1. Published after 2020 (year > 2020)
    2. Each paper must have >= 100 citations
    3. Include metadata: title, authors, year, citation_count, and URL
    4. Try to find at least 3 papers
    5. Provide a summary explaining transformer applications
    6. Return STRICTLY in JSON format as:
    {
      "papers": [
        {"title": "...", "authors": ["..."], "year": 20XX, "citation_count": XXX, "url": "..."}
      ],
      "summary": "..."
    }
    7. Only return JSON. Do NOT add extra text.
    """

def use_case_2():
    return """
    Find research papers on "climate change adaptation" with constraints:
    1. Published after 2020 (year > 2020)
    2. Each paper must have >= 30 citations
    3. Include metadata: title, authors, year, citation_count, and URL
    4. Try to find at least 3 papers
    5. Provide summary of climate solutions discussed
    6. Return STRICTLY in JSON format as:
    {
      "papers": [
        {"title": "...", "first_author": "...", "year": 20XX, "citation_count": XXX, "url": "..."}
      ],
      "summary": "..."
    }
    7. Only return JSON. Do NOT add extra text.
    """

def use_case_3():
    return """
    Find research papers on "AI medical diagnosis" with constraints:
    1. Published after 2019 (year > 2019)
    2. Each paper must have >= 50 citations
    3. Include metadata: title, authors, year, citation_count, and URL
    4. Try to find at least 3 papers
    5. Provide summary of diagnostic applications
    6. Return STRICTLY in JSON format as:
    {
      "papers": [
        {"title": "...", "authors": ["..."], "year": 20XX, "citation_count": XXX, "url": "..."}
      ],
      "summary": "..."
    }
    7. Only return JSON. Do NOT add extra text.
    """