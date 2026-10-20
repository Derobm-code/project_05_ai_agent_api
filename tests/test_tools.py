import unittest

from tools import(calculate_percentage, add_numbers, 
                  multiply_numbers, subtract_numbers, calculate_remaining_after_reduction,)

class TestTools(unittest.TestCase):
    def test_calculate_percentage(self):
        self.assertAlmostEqual(
            calculate_percentage(840, 25), 210.0,
        )

    def test_add_numbers(self):
        self.assertAlmostEqual(add_numbers(210, 100), 310.0)

    def test_multiply_numbers(self):
        self.assertAlmostEqual(multiply_numbers(25, 16), 400.0)

    def test_subtract_numbers(self):
        self.assertAlmostEqual(subtract_numbers(840, 210), 630.0)

    def test_percentage_reduction(self):
        result= calculate_remaining_after_reduction(840,25)

        self.assertAlmostEqual(result["amount_reduced"], 210.0)
        self.assertAlmostEqual(result["remaining_value"], 630.0)

if __name__ == "__main__":
    unittest.main()