import math

from main import run_agent

def find_step(trace: list[dict], tool_name: str):
    return next(
        (step for step in trace if step["tool"] == tool_name),
        None,
    )

def tools_appear_in_order(
        trace: list[dict],
        expected_tools: list[str],
) -> bool:
    actual_tools = [step["tool"] for step in trace]
    position = 0

    for tool_name in actual_tools:
        if (
            position < len(expected_tools)
            and tool_name == expected_tools[position]
        ):
            position += 1
    return position == len(expected_tools)

def numeric_result_is(
    trace: list[dict],
    tool_name: str,
    expected: float,
) -> bool:
    step = find_step(trace, tool_name)

    if step is None:
        return False

    result = step["result"]

    if not isinstance(result, (int, float)):
        return False

    return math.isclose(float(result), expected, abs_tol=1e-9)

def evaluate_case(
    name: str,
    prompt: str,
    expected_tools: list[str],
    result_check,
    
) -> bool:
    print(f"\n{'=' * 50}")
    print(f"TEST: {name}")
    print("=" * 50)

    try: 
        answer, trace = run_agent(prompt)

        tools_ok = tools_appear_in_order(trace, expected_tools)
        result_ok = result_check(answer, trace)

        passed = tools_ok and result_ok

        print("Expected tools:", expected_tools)
        print("Observed tools:", [step["tool"] for step in trace])
        print("Correct tool sequence:", tools_ok)
        print("Correct results and answer:", result_ok)
        print("Result:", "PASS" if passed else "FAIL")


        if not passed:
            print("Answer:", answer)

        return passed
    
    except Exception as exc:
        print("Result: ERROR")
        print(f"Details: {exc}")
        return False

def check_percentage(answer: str, trace: list[dict]) -> bool:
    return (
        numeric_result_is(trace, "calculate_percentage", 210)
        and "210" in answer
    )

def check_sequential_calculation(
    answer: str,
    trace: list[dict],
) -> bool:
    return(
        numeric_result_is(trace, "calculate_percentage", 210)
        and numeric_result_is(trace, "add_numbers", 310)
        and "310" in answer
    )

def check_rag_calculation(
    answer: str,
    trace: list[dict],
) -> bool:
    retrieval = find_step(trace, "search_knowledge_base")
    calculation = find_step(
        trace, "calculate_remaining_after_reduction",
    )

    if retrieval is None or calculation is None:
        return False

    retrieval_ok = "automation.txt" in str(retrieval["result"])

    result = calculation["result"]

    calculation_ok = (
        isinstance(result, dict)
        and math.isclose(
            float(result.get("amount_reduced", -1)),
            210,
            abs_tol=1e-9,
        )
        and math.isclose(
            float(result.get("remaining_value", -1)),
            630,
            abs_tol=1e-9,
        )
    )

    answer_ok = "210" in answer and "630" in answer

    return retrieval_ok and calculation_ok and answer_ok

def main():
    cases = [
        (
            "Simple percentage",
            "What is 25% of 840?",
            ["calculate_percentage"],
            check_percentage,
        ),
        (
            "Sequential calculation",
            "Calculate 25% of 840 and then add 100 to that result.",
            ["calculate_percentage", "add_numbers"],
            check_sequential_calculation,
        ),
        (
            "Knowledge retrieval and percentage reduction",
            (
                "According to my knowledge base, Python is used for "
                "automation. If a task takes 840 seconds and its duration " 
                "is reduced by 25%, how much time is saved and how long ramins?"
            ),
            [
                "search_knowledge_base",
                "calculate_remaining_after_reduction",
            ],
            check_rag_calculation,
        ),
    ]

    results = [
        evaluate_case(name, prompt, expected_tools, check)
        for name, prompt, expected_tools, check in cases
    ]

    passed = sum(results)
    failed = len(results) - passed

    print(f"\n{'=' * 50}")
    print("PROJECT 3 - END-TO-END AGENT EVALUATION")
    print("=" * 50)
    print(f"Scenarios: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("FINAL RESULT = PASS")
        return 0
    
    print("FINAL_RESULT: FAIL")
    return 1
    
if __name__ == "__main__":
    raise SystemExit(main())
