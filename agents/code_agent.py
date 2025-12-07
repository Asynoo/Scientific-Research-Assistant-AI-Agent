from autogen import ConversableAgent

from config import LLM_CONFIG


def create_code_agent():
    system_msg = (
        "You are a code-execution assistant. FLOW:\n"
        "1) You receive a JSON string from ResearchAgent (as a content string).\n"
        "2) You MUST generate Python code (as the tool parameter) which parses that JSON and prints a final JSON\n"
        "   with keys: {\"table\": [...], \"analysis\": \"...\"} to stdout.\n"
        "3) The code must be minimal and robust (use json.loads, handle missing keys).\n"
        "4) DO NOT call external services. Do NOT output anything else besides the code block for the 'execute_code' tool.\n"
        "After the tool runs, return the tool output and then TERMINATE."
    )

    agent = ConversableAgent(
        name="Code Agent",
        system_message=system_msg,
        llm_config=LLM_CONFIG
    )

    return agent
