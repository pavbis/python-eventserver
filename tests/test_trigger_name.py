from unittest import TestCase
from eventsserver.value.objects import TriggerName, InvalidArgument


class TriggerNameTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            TriggerName(primitive_value)
        self.assertTrue('Trigger name cannot be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test'
        trigger_name = TriggerName(primitive_value)

        self.assertEqual(primitive_value, str(trigger_name))
