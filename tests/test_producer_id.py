from unittest import TestCase
from eventsserver.value.objects import ProducerId, InvalidArgument


class ProducerIdTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_invalid_uuid(self):
        primitive_value = 'invalid'

        with self.assertRaises(InvalidArgument) as context:
            ProducerId(primitive_value)
        self.assertTrue('invalid uuid provided.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'd9e0236f-2a93-4a4e-8026-f46d9605a5fb'
        file_name = ProducerId(primitive_value)

        self.assertEqual(primitive_value, str(file_name))
