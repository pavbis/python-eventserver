from unittest import TestCase
from calculator.simple_calculator import add


class CalcTest(TestCase):

    def test_returns_sum(self):
        result = add(2, 3)
        self.assertEqual(5, result)