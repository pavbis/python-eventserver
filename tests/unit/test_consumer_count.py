from unittest import TestCase
from eventsserver.value.objects import ConsumerCount, InvalidArgument


class ConsumerCountTest(TestCase):
    def test_it_raises_error_if_primitive_value_lower_than_one(self):
        with self.assertRaises(InvalidArgument) as context:
            ConsumerCount(-1)
        self.assertTrue('Consumer count cannot be lower than zero.' in str(context.exception))

    def test_it_returns_the_primitive_value(self):
        primitive_value = 1
        consumer_count = ConsumerCount(primitive_value)

        self.assertEqual(primitive_value, int(consumer_count))
