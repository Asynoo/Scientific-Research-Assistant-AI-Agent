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
        name="User Proxy / Agent",
        llm_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content", "").strip().endswith("TERMINATE")
    )
    user.register_for_execution(name="search_papers")(search_papers)
    user.register_for_execution(name="execute_code")(execute_code)
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
    print(f"RUNNING: {case_name}")
    print(f"{'=' * 60}")

    user = create_user_proxy()
    research = create_research_agent()
    code_agent = create_code_agent()
    evaluator = create_evaluator_agent()

    print("\n[1] Research")
    r_out = safe_initiate(user, research, task, max_turns=2)
    print(r_out[:1000] + "..." if len(r_out) > 1000 else r_out)
    r_json = extract_json(r_out)

    if not r_json:
        print("No JSON from research")
        return None

    print("\n[2] Code")

    if not r_json.get("papers", []):
        print("No papers, skip code")
        code_json = r_json
    else:
        code_prompt = f"JSON_INPUT:\n{json.dumps(r_json)}\nWrite Python script."
        code_reply = safe_initiate(user, code_agent, code_prompt, max_turns=1)

        script = code_reply.replace("```python", "").replace("```", "").strip()
        exec_out = execute_code(script)

        if exec_out.get("success"):
            print("Code OK")
            code_json = extract_json(exec_out.get("stdout", ""))
            if not code_json:
                code_json = r_json
        else:
            print(f"Code failed: {exec_out.get('error')}")
            return None

    print("\n[3] Evaluation")
    eval_prompt = f"Check these papers against task requirements:\n\nTASK: {task}\n\nPAPERS FOUND:\n{json.dumps(code_json, indent=2)}\n\nDo ALL papers meet the citation and year requirements? Output JSON."
    eval_out = safe_initiate(user, evaluator, eval_prompt, max_turns= 1)
    print(eval_out)

    return {
        "case_name": case_name,
        "research_output": r_json,
        "code_output": code_json,
        "evaluation": eval_out
    }


def main():
    all_results = []

    # Simply comment/un-comment depending on which cases you wish to run.
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
    print(f"DONE: {len(all_results)}/{len(cases)}")
    print(f"Saved to test_results.json")

    for result in all_results:
        eval_json = extract_json(result["evaluation"])
        if eval_json:
            success = eval_json.get("success", False)
            print(f"{result['case_name']}: {'PASS' if success else 'FAIL'}")


if __name__ == "__main__":
    main()