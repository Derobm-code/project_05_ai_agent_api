import unittest

from pydantic import ValidationError

from main import execute_tool, requires_knowledge_base

class TestAgentLogic(unittest.TestCase):
    def test_calculate_percentage_dispatch(self):
        result = execute_tool(
            "calculate_percentage",
            {"value": 840, "percentage": 25},
        )
        self.assertAlmostEqual(result, 210.0)

    def test_percentage_reducation_dispatch(self):
        result = execute_tool(
            "calculate_remaining_after_reduction",
            {"value": 840, "percentage": 25},
        )
        self.assertAlmostEqual(result["amount_reduced"], 210.0)
        self.assertAlmostEqual(result["remaining_value"], 630.0)

    def test_invalid_percentage_is_rejected(self):
        with self.assertRaises(ValidationError):
            execute_tool(
                "calculate_percentage",
                {"value": 840, "percentage": -25},
            )

    def test_unknown_tool_is_rejected(self):
        with self.assertRaises(ValueError):
            execute_tool("unknown_tool", {})

    def test_knowledge_base_request_is_detected(self):
        self.assertTrue(
            requires_knowledge_base(
                "According to my knowledge base, what is Python?"
            )
        )
    def test_normal_calculation_does_not_require_rag(self):
        self.assertFalse(
            requires_knowledge_base("What is 25% of 840")
        )

if __name__ == "__main__":
    unittest.main()
    