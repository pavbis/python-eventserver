import unittest
from calculator.simple_calculator import Calc


class CalcTest(unittest.TestCase):

    def setUp(self):
        self.calculator = Calc()

    def test_returns_sum(self):
        result = self.calculator.add(2, 3)
        self.assertEqual(5, result)


if __name__ == '__main__':
    unittest.main()
