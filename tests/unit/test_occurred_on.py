from unittest import TestCase
from datetime import datetime
from eventsserver.value.objects import OccurredOn


class OccurredOnTest(TestCase):
    def test_occurred_on_returns_date_time_as_string(self) -> None:
        primitive_date_time_string = '2019-11-03 08:22:40.384000+00:00'
        date_time = datetime.fromisoformat(primitive_date_time_string)
        occurred_on = OccurredOn(date_time)

        self.assertEqual(primitive_date_time_string, str(occurred_on))
