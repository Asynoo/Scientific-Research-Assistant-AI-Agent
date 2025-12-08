from autogen import ConversableAgent
from config import LLM_CONFIG

def create_evaluator_agent():
    system_msg = (
        "You are a practical evaluator.\n"
        "RULES:\n"
        "- Check if papers meet basic constraints: year and citation requirements FROM THE TASK.\n"
        "- If task says 'citation_count >= 30', check the 'citation_count' field in each paper.\n"
        "- Allow flexible field names (first_author/top_author are both acceptable).\n"
        "- Check if summary/analysis is provided and relevant.\n"
        "- If no papers found, check if agent properly reported 'no results'.\n"
        "- Output ONLY JSON: {\"success\": boolean, \"reason\": \"...\"}.\n"
        "- After JSON, output the exact string: TERMINATE on a new line.\n"
        "- Be reasonable - real APIs may return limited results.\n"
        "- Do NOT provide any extra explanation or text."
    )

    return ConversableAgent(
        name="Evaluator Agent",
        system_message=system_msg,
        llm_config=LLM_CONFIG
    )