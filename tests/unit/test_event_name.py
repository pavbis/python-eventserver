from unittest import TestCase
from eventsserver.value.objects import EventName, InvalidArgument


class EventNameTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            EventName(primitive_value)
        self.assertTrue('event name can not not be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test'
        event_name = EventName(primitive_value)

        self.assertEqual(primitive_value, str(event_name))
