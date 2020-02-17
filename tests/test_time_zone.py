from unittest import TestCase
from eventsserver.value.objects import TimeZone, InvalidArgument


class TimeZoneTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_invalid_uuid(self):
        primitive_value = 'invalid/zone'

        with self.assertRaises(InvalidArgument) as context:
            TimeZone(primitive_value)
        self.assertTrue('Unknown or bad timezone.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'Europe/Berlin'
        time_zone = TimeZone(primitive_value)

        self.assertEqual(primitive_value, str(time_zone))
