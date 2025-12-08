from autogen import ConversableAgent
from config import LLM_CONFIG

def create_code_agent():
    system_msg = (
        "You are a Python code-execution assistant.\n"
        "OUTPUT RULES:\n"
        "- Respond with ONLY ONE valid Python script.\n"
        "- Do NOT include markdown, backticks, or explanations.\n"
        "- The script must:\n"
        "    1. Store a variable JSON_INPUT as a triple-quoted string.\n"
        "    2. Parse it with json.loads.\n"
        "    3. Create output that PRESERVES ORIGINAL FIELD NAMES from input.\n"
        "    4. DO NOT ADD FIELDS THAT DON'T EXIST IN THE INPUT.\n"
        "    5. If input has 'first_author', keep it as 'first_author'.\n"
        "    6. If input has 'lead_institution', keep it as 'lead_institution'.\n"
        "    7. If input has 'authors' list, transform to 'top_author' as first author.\n"
        "    8. Compute 'analysis' as a summary text string (use the existing summary).\n"
        "    9. Print a JSON object with same structure as input but transformed fields.\n"
        "- Handle missing keys gracefully.\n"
        "- DO NOT INVENT DATA - use only what's provided.\n"
        "- After outputting the script, do NOT respond further."
    )

    return ConversableAgent(
        name="Code Agent",
        system_message=system_msg,
        llm_config=LLM_CONFIG
    )