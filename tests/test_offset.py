from unittest import TestCase
from eventsserver.value.objects import Offset, InvalidArgument


class OffsetTest(TestCase):
    def test_it_raises_error_if_primitive_value_lower_than_one(self):
        with self.assertRaises(InvalidArgument) as context:
            Offset(-12)
        self.assertTrue('Offset cannot be lower than zero.' in str(context.exception))

    def test_it_returns_the_primitive_value(self):
        primitive_value = 1
        offset = Offset(primitive_value)

        self.assertEqual(primitive_value, int(offset))

        offset.increment()

        self.assertEqual(2, int(offset))

    def test_equals_return_false_if_primitives_are_not_equal(self):
        first_offset = Offset(1)
        second_offset = Offset(2)

        self.assertFalse(first_offset.__eq__(second_offset))

    def test_equals_return_true_if_primitives_are_equal(self):
        first_offset = Offset(1)
        second_offset = Offset(1)

        self.assertTrue(first_offset.__eq__(second_offset))
