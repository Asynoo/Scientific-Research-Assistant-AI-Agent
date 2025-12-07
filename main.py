import json
import re
import time
import traceback

from autogen import ConversableAgent

from agents.code_agent import create_code_agent
from agents.evaluator_agent import create_evaluator_agent
from agents.research_agent import create_research_agent
from tools.code_executor import execute_code
from tools.paper_search_tool import search_papers


def create_user_proxy():
    user = ConversableAgent(
        name="UserProxy",
        llm_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg.get("content")
    )

    user.register_for_execution(name="execute_code")(execute_code)
    user.register_for_execution(name="search_papers")(search_papers)
    return user


def safe_initiate(user_proxy, agent, message, max_turns=5, max_retries=3):
    for attempt in range(max_retries):
        try:
            user_proxy.initiate_chat(agent, message=message, max_turns=max_turns)
            return user_proxy.last_message(agent)["content"]
        except Exception as e:
            err = str(e)
            if "Rate limit" in err or "rate" in err.lower() or "429" in err:
                wait = 2 ** attempt
                print(f"[WARN] Rate-limited / transient error. Retry in {wait}s (attempt {attempt + 1}/{max_retries}).")
                time.sleep(wait)
                continue
            else:
                print("[ERROR] Non-retryable exception in safe_initiate:")
                traceback.print_exc()
                raise
    raise RuntimeError("Max retries exceeded in safe_initiate")


def extract_json_from_text(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("[ERROR] Failed to extract JSON:", e)
    return None


def main():
    task = "Find 5 research papers on cybersecurity that were published after 2017 and have at least 100 citations each."

    user = create_user_proxy()
    research_agent = create_research_agent()
    code_agent = create_code_agent()
    evaluator_agent = create_evaluator_agent()

    print("\n--- STEP 1: ResearchAgent (search) ---")
    research_out = safe_initiate(user, research_agent, message=task, max_turns=5)
    print("ResearchAgent output (raw):\n", research_out)

    research_json = extract_json_from_text(research_out)
    if research_json is None:
        print("[ERROR] Could not parse ResearchAgent output as JSON.")
        return

    print("\n--- STEP 2: CodeAgent (produce and execute code) ---")
    code_prompt = (
        "You will be given a JSON string (from ResearchAgent). Produce a Python script that:\n"
        " - Parses the JSON\n"
        " - Builds a list 'table' of dicts with keys: title, year, citation_count, url, top_author\n"
        " - Produces a JSON to stdout: {\"table\": table, \"analysis\": \"...\"}\n"
        " - Handle missing keys gracefully.\n"
        "\nJSON_INPUT:\n"
        f"{json.dumps(research_json)}\n\n"
        "Remember: produce only the Python code to be executed (no surrounding markdown)."
    )

    code_out = safe_initiate(user, code_agent, message=code_prompt, max_turns=5)
    print("CodeAgent returned (should be Python code):\n", code_out)

    code_text = code_out
    if "```" in code_text:
        code_text = code_text.replace("```python", "```").split("```")
        if len(code_text) >= 3:
            code_text = code_text[1]
        else:
            code_text = "".join(code_text)

    print("\n--- STEP 2b: executing code via UserProxy.execute_code ---")
    try:
        exec_result = execute_code(code_text)
        print("Execution result:", exec_result)
        code_output = exec_result.get("stdout", "")
        if not exec_result.get("success"):
            print("[WARN] Code execution failed or returned non-zero exit code.")
    except Exception:
        print("[ERROR] Exception while executing code:")
        traceback.print_exc()
        return

    code_json = extract_json_from_text(code_output)
    if code_json is None:
        print("[ERROR] Cannot parse code execution output as JSON. Raw stdout:")
        print(code_output)

    print("\n--- STEP 3: EvaluatorAgent (one-shot) ---")
    eval_prompt = (
        f"TASK: {task}\n\n"
        f"AGENT RESULT: {json.dumps(research_json)}\n\n"
        "EVALUATION CRITERIA:\n"
        "1) Did the agent find real papers (non-empty urls)?\n"
        "2) Are papers published after the year specified?\n"
        "3) Do papers meet the citation threshold?\n\n"
        "Output ONLY JSON {\"success\": boolean, \"reason\": \"...\"} and then TERMINATE."
    )

    try:
        eval_out = safe_initiate(user, evaluator_agent, message=eval_prompt, max_turns=3)
        print("Evaluator output:\n", eval_out)
    except Exception as e:
        print("[ERROR] Evaluator failed:", e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
