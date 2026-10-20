from pathlib import Path
import unittest

from evaluate_agent import main as run_agent_evaluation

PROJECT_ROOT = Path(__file__).resolve().parent
TESTS_DIR = PROJECT_ROOT / "tests"

def run_unit_tests() -> bool:
    print("\n" + "=" * 50)
    print("UNIT TESTS")
    print("=" * 50, flush=True)

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(TESTS_DIR),
        pattern="test_*.py",
        top_level_dir=str(PROJECT_ROOT),
    )

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def main() -> int:
    # Run deterministic Python, Scheoma, and retrival tests
    unit_tests_passed = run_unit_tests()

    # Run scenarios against the actual local LLM agent
    print("\n" + "=" * 50)
    print("END-TO-END AGENT_TESTS")
    print("=" * 50, flush=True)

    agent_exit_code = run_agent_evaluation()
    agent_tests_passed = agent_exit_code == 0

    # Combined report
    print("\n" + "=" * 50)
    print("PROJECT 3 - COMBINED EVALUATION")
    print("=" * 50)
    print(
        "Unit tests: ",
        "PASS" if unit_tests_passed else "FAIL",
    )
    print(
        "Agent tests:",
        "PASS" if agent_tests_passed else "FAIL",
    )

    overall_passed = unit_tests_passed and agent_tests_passed

    print("-" * 50)
    print(
        "FINAL RESULT:",
        "PASS" if overall_passed else "FAIL",
    )

    return 0 if overall_passed else 1

if __name__ == "__main__":
    raise SystemExit(main())

    