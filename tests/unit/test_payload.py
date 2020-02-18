from unittest import TestCase
from eventsserver.value.objects import PayLoad, InvalidArgument


class PayloadTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            PayLoad(primitive_value)
        self.assertTrue('Payload must be an dict.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = {'one': 1, 'two': 2, 'three': {'three.1': 3.1, 'three.2': 3.2}}
        payload = PayLoad(primitive_value)

        self.assertEqual("{'one': 1, 'two': 2, 'three': {'three.1': 3.1, 'three.2': 3.2}}", str(payload))
