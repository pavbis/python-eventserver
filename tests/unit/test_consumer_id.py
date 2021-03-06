from unittest import TestCase
from eventsserver.value.objects import ConsumerId, InvalidArgument


class ConsumerIdTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_invalid_uuid(self):
        primitive_value = 'invalid'

        with self.assertRaises(InvalidArgument) as context:
            ConsumerId(primitive_value)
        self.assertTrue('invalid uuid provided.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'd9e0236f-2a93-4a4e-8026-f46d9605a5fb'
        consumer_id = ConsumerId(primitive_value)

        self.assertEqual(primitive_value, str(consumer_id))
