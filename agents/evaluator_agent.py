from autogen import ConversableAgent

from config import LLM_CONFIG


def create_evaluator_agent():
    system_msg = (
        "You are a strict evaluator. INPUT: TASK (text) and AGENT RESULT (either JSON or text).\n"
        "INSTRUCTIONS:\n"
        "- Check ONLY explicit constraints in TASK. Do NOT invent hidden constraints.\n"
        "- Example: 'published after 2017' means year >= 2018 counts.\n"
        "- If TASK contains numeric thresholds, compare them exactly.\n"
        "- Output ONLY valid JSON: {\"success\": boolean, \"reason\": \"detailed explanation\"}\n"
        "- Then on a new line output the literal string TERMINATE.\n"
    )

    return ConversableAgent(
        name="Evaluator Agent",
        system_message=system_msg,
        llm_config=LLM_CONFIG
    )
