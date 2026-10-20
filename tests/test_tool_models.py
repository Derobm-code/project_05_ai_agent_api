import unittest

from pydantic import ValidationError

from tool_models import (CalculatePercentageArgs, TwoNumbersArgs, PercentageReductionArgs,
                         SearchKnowledgeBaseArgs,)

class TestToolModels(unittest.TestCase):

    def test_valid_percentage_arguments(self):
        args = CalculatePercentageArgs.model_validate({
            "value": 840,
            "percentage": 25,
        })
        self.assertAlmostEqual(args.value, 840)
        self.assertAlmostEqual(args.percentage, 25)

    def test_negative_percentage_is_rejected(self):
        with self.assertRaises(ValidationError):
            CalculatePercentageArgs.model_validate({
                "value": 840,
                "percentage": -25,
            })
    def test_mission_required_argument_is_rejected(self):
        with self.assertRaises(ValidationError):
            CalculatePercentageArgs.model_validate({
                "percentage": 25,
            })
    def test_non_numeric_value_is_rejected(self):
        with self.assertRaises(ValidationError):
            TwoNumbersArgs.model_validate({
                "a": "hello",
                "b": 10,
            })
    def test_percentage_reduction_over_100_is_rejected(self):
        with self.assertRaises(ValidationError):
            PercentageReductionArgs.model_validate({
                "value": 840,
                "percentage": 125,
            })
    def test_valid_percentage_reduction(self):
        args = PercentageReductionArgs.model_validate({
            "value": 840,
            "percentage": 25,
        })

        self.assertEqual(args.value, 840)
        self.assertEqual(args.percentage, 25)

    def test_valid_knowledge_base_query(self):
        args = SearchKnowledgeBaseArgs.model_validate({
            "query": "How is Python used for automation?",
        })

        self.assertEqual(args.query, "How is Python used for automation?",)


if __name__ == "__main__":
    unittest.main()
