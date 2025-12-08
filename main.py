import json
import re
import time
from autogen import ConversableAgent
from agents.code_agent import create_code_agent
from agents.evaluator_agent import create_evaluator_agent
from agents.research_agent import create_research_agent
from tools.code_executor import execute_code
from tools.paper_search_tool import search_papers
from use_cases import use_case_1, use_case_2, use_case_3


def create_user_proxy():
    user = ConversableAgent(
        name="UserProxy",
        llm_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content", "").strip().endswith("TERMINATE")
    )
    user.register_for_execution("execute_code")(execute_code)
    user.register_for_execution("search_papers")(search_papers)
    return user


def safe_initiate(user_proxy, agent, message, max_turns=3, max_retries=3):
    for attempt in range(max_retries):
        try:
            user_proxy.initiate_chat(agent, message=message, max_turns=max_turns)
            return user_proxy.last_message(agent)["content"]
        except Exception as e:
            if "429" in str(e) or "rate" in str(e).lower():
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError("Too many retries")


def extract_json(text):
    try:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group())
    except:
        pass
    return None


def run_single_case(case_name, task):
    print(f"\n{'=' * 60}")
    print(f"RUNNING USE CASE: {case_name}")
    print(f"{'=' * 60}")

    user = create_user_proxy()
    research = create_research_agent()
    code_agent = create_code_agent()
    evaluator = create_evaluator_agent()

    print("\n--- STEP 1: Research ---")
    r_out = safe_initiate(user, research, task)
    print(r_out[:1000] + "..." if len(r_out) > 1000 else r_out)
    r_json = extract_json(r_out)

    if not r_json:
        print("Failed to extract JSON from research agent")
        return None

    print("\n--- STEP 2: Code Execution ---")

    if not r_json.get("papers", []):
        print("No papers found, skipping code execution")
        code_json = r_json
    else:
        code_prompt = "JSON_INPUT:\n" + json.dumps(r_json) + "\nProduce the Python script now."
        code_reply = safe_initiate(user, code_agent, code_prompt)

        script = code_reply.replace("```python", "").replace("```", "").strip()
        exec_out = execute_code(script)

        if exec_out.get("success"):
            print(f"Code executed successfully")
            code_json = extract_json(exec_out.get("stdout", ""))
            if not code_json:
                print("Warning: Could not extract JSON from code output")
                code_json = r_json
        else:
            print(f"Code execution failed: {exec_out.get('error')}")
            return None

    print("\n--- STEP 3: Evaluation ---")
    eval_prompt = (
        f"TASK: {task}\n\n"
        f"AGENT RESULT: {json.dumps(code_json)}\n\n"
        "Output JSON only and TERMINATE."
    )
    eval_out = safe_initiate(user, evaluator, eval_prompt)
    print(eval_out)

    return {
        "case_name": case_name,
        "research_output": r_json,
        "code_output": code_json,
        "evaluation": eval_out
    }


def main():
    all_results = []

    cases = [
        ("ML Transformers", use_case_1()),
        ("Climate Change", use_case_2()),
        ("Healthcare AI", use_case_3())
    ]

    for case_name, task in cases:
        result = run_single_case(case_name, task)
        if result:
            all_results.append(result)

    with open("test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"COMPLETED {len(all_results)}/{len(cases)} USE CASES")
    print(f"Results saved to test_results.json")

    for result in all_results:
        eval_json = extract_json(result["evaluation"])
        if eval_json:
            success = eval_json.get("success", False)
            print(f"{result['case_name']}: {'PASS' if success else 'FAIL'}")


if __name__ == "__main__":
    main()