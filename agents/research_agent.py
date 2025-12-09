from autogen import ConversableAgent

from config import LLM_CONFIG
from tools.paper_search_tool import search_papers


def create_research_agent():
    system_msg = (
        "You are a precise research paper agent.\n"
        "You MUST call the tool 'search_papers' exactly once.\n"
        "CRITICAL FILTERING RULES:\n"
        "1. When you receive papers from the tool, FILTER them to keep ONLY papers that meet ALL constraints:\n"
        "   - Year > specified year\n"
        "   - Citation count >= specified minimum\n"
        "2. Return EXACTLY 5 papers that meet these criteria.\n"
        "3. If fewer than 5 papers meet criteria, return ALL papers that meet criteria.\n"
        "4. Do NOT include any paper that fails any constraint.\n"
        "5. DO NOT INVENT PAPERS - only return papers from the tool results.\n"
        "6. ALWAYS include 'authors' field as a list, even if user asks for 'first_author'.\n"
        "\n"
        "PARAMETERS you may use: topic, year_filter, year, min_citations.\n"
        "\n"
        "After filtering, output STRICT JSON only (no markdown, no extra text):\n"
        "{\n"
        "  'papers': [{'title': '...', 'authors': [...], 'year': ..., 'citation_count': ..., 'url': '...'}],\n"
        "  'summary': 'Found X papers meeting all constraints. Summary: ...'\n"
        "}\n"
        "Then output TERMINATE on a new line."
    )

    agent = ConversableAgent(
        name="Research Agent",
        system_message=system_msg,
        llm_config=LLM_CONFIG
    )

    agent.register_for_llm(
        name="search_papers",
        description="Search for papers. Parameters: topic, year_filter, year."
    )(search_papers)

    return agent
