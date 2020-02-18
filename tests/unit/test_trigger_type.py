from unittest import TestCase
from eventsserver.value.objects import TriggerType, InvalidArgument


class TriggerTypeTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            TriggerType(primitive_value)
        self.assertTrue('Trigger type cannot be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test'
        trigger_type = TriggerType(primitive_value)

        self.assertEqual(primitive_value, str(trigger_type))
