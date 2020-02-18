from unittest import TestCase
from eventsserver.value.objects import EventVersion, InvalidArgument


class EventVersionTest(TestCase):
    def test_it_raises_error_if_primitive_value_lower_than_one(self):
        with self.assertRaises(InvalidArgument) as context:
            EventVersion(-1)
        self.assertTrue('Event version cannot be lower than 1.' in str(context.exception))

    def test_it_returns_the_primitive_value(self):
        primitive_value = 1
        event_version = EventVersion(primitive_value)

        self.assertEqual(primitive_value, int(event_version))
