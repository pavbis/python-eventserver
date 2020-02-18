from unittest import TestCase
from eventsserver.value.objects import EventCount, InvalidArgument


class EventCountTest(TestCase):
    def test_it_raises_error_if_primitive_value_lower_than_one(self):
        with self.assertRaises(InvalidArgument) as context:
            EventCount(-12)
        self.assertTrue('Event count cannot be lower than zero.' in str(context.exception))

    def test_it_returns_the_primitive_value(self):
        primitive_value = 1
        event_count = EventCount(primitive_value)

        self.assertEqual(primitive_value, int(event_count))
