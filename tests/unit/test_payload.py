from unittest import TestCase
from eventsserver.value.objects import PayLoad, InvalidArgument


class PayloadTest(TestCase):
    def setUp(self) -> None:
        self.payload = PayLoad({'one': 1, 'two': 2, 'three': {'three.1': 3.1, 'three.2': 3.2}})

    def test_it_returns_provided_primitive_value_as_json(self):
        self.assertEqual('{"one": 1, "two": 2, "three": {"three.1": 3.1, "three.2": 3.2}}', self.payload.to_json())

    def test_it_returns_provided_primitive_value(self):
        self.assertEqual("{'one': 1, 'two': 2, 'three': {'three.1': 3.1, 'three.2': 3.2}}", str(self.payload))
