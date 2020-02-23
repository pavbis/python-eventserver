from unittest import TestCase
from eventsserver.value.objects import InvalidArgument, AggregatedJson


class AggregatedJsonTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_invalid_json(self):
        primitive_value = '(7hhf'

        with self.assertRaises(InvalidArgument) as context:
            AggregatedJson(primitive_value)
        self.assertTrue('Value is not a JSON string.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = '{"event": {"id": "c3f390b8-302f-49af-b987-66ab0a931a62", "name": "Snickers", "version": ' \
                          '1}, "system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", ' \
                          '"timezone": "Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", ' \
                          '"type": "system"}}'

        aggregated_json = AggregatedJson(primitive_value)

        self.assertEqual(primitive_value, str(aggregated_json))

