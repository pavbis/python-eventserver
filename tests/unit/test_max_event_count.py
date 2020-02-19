from unittest import TestCase
from eventsserver.value.objects import MaxEventCount, InvalidArgument


class MaxEventCountTest(TestCase):
    def test_it_raises_error_if_primitive_value_lower_than_one(self):
        with self.assertRaises(InvalidArgument) as context:
            MaxEventCount(0)
        self.assertTrue('Max consume count must be greater than 0.' in str(context.exception))

    def test_it_returns_the_primitive_value(self):
        primitive_value = 1
        event_count = MaxEventCount(primitive_value)

        self.assertEqual(primitive_value, int(event_count))
