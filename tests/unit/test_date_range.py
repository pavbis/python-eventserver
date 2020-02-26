from datetime import datetime
from unittest import TestCase
from eventsserver.value.objects import InvalidArgument, DateRange


class DateRangeTest(TestCase):
    def test_it_raises_exception_if_start_date_is_greater_than_end_date(self):
        start_date = datetime.fromisoformat('2019-12-04')
        end_date = datetime.fromisoformat('2019-12-03')

        with self.assertRaises(InvalidArgument) as context:
            DateRange(start_date, end_date).is_valid()
        self.assertTrue('End date must be greater than start date.' in str(context.exception))

    def test_it_returns_true_if_end_date_is_greater_than_start_date(self):
        start_date = datetime.fromisoformat('2019-12-04')
        end_date = datetime.fromisoformat('2019-12-05')
        date_range = DateRange(start_date, end_date)

        self.assertTrue(date_range.is_valid())
        self.assertEqual(start_date, date_range.get_start())
        self.assertEqual(end_date, date_range.get_end())

