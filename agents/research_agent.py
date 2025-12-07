from autogen import ConversableAgent

from config import LLM_CONFIG
from tools.paper_search_tool import search_papers


def create_research_agent():
    system_msg = (
        "You are a precise research paper finding agent.\n"
        "INSTRUCTIONS:\n"
        "- Call the tool 'search_papers' exactly ONCE per request.\n"
        "- After receiving the tool response, OUTPUT ONLY valid JSON (no markdown, no extra text).\n"
        "Output schema EXACTLY:\n"
        "{\n"
        "  \"papers\": [\n"
        "    {\"title\": \"...\", \"authors\": [...], \"year\": 2023, \"citation_count\": 123, \"url\": \"...\"}\n"
        "  ],\n"
        "  \"summary\": \"short summary (max 6 sentences)\"\n"
        "}\n"
        "Then on a new line output the literal string TERMINATE."
    )

    agent = ConversableAgent(
        name="Research Agent",
        system_message=system_msg,
        llm_config=LLM_CONFIG
    )

    agent.register_for_llm(
        name="search_papers",
        description="Search for research papers. Parameters: topic, year_filter, year, citation_filter, citation_count"
    )(search_papers)

    return agent
