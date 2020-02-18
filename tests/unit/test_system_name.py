from unittest import TestCase
from eventsserver.value.objects import SystemName, InvalidArgument


class SystemNameTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            SystemName(primitive_value)
        self.assertTrue('System name cannot be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test'
        system_name = SystemName(primitive_value)

        self.assertEqual(primitive_value, str(system_name))
