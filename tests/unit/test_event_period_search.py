from datetime import datetime
from unittest import TestCase
from eventsserver.value.objects import Period, DateRange
from eventsserver.search.event_period_search import EventPeriodSearch
from eventsserver.search.event_period_search import UnsupportedPeriod
from eventsserver.search.search_specifications_list import SearchSpecificationsList
from eventsserver.search.specifications.period_specifications import (
    LastWeekSpecification,
    LastTwoWeeksSpecification,
    LastTwoDaysSpecification,
    LastSixHoursSpecification,
    LastMonthSpecification,
    LastDaySpecification,
    EmptyPeriodSpecification,
    DateRangeSpecification
)


class EventPeriodTest(TestCase):
    def setUp(self) -> None:
        specifications_list = SearchSpecificationsList().all_with_interval()

        self.event_period_search = EventPeriodSearch(specifications_list)

    def test_it_raises_exception_if_period_is_invalid(self) -> None:
        period = Period('invalid')

        with self.assertRaises(UnsupportedPeriod) as context:
            self.event_period_search.find_specification(period=period)
        self.assertTrue('Period "{}" is not supported or invalid.'.format(str(period)) in str(context.exception))

    def test_it_returns_last_week_specification(self) -> None:
        period = Period('7 day')

        specification = self.event_period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, LastWeekSpecification)

    def test_it_returns_last_two_weeks_specification(self) -> None:
        period = Period('14 day')

        specification = self.event_period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, LastTwoWeeksSpecification)

    def test_it_returns_last_two_days_specification(self) -> None:
        period = Period('2 day')

        specification = self.event_period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, LastTwoDaysSpecification)

    def test_it_returns_last_six_hours_specification(self) -> None:
        period = Period('6 hour')

        specification = self.event_period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, LastSixHoursSpecification)

    def test_it_returns_last_month_specification(self) -> None:
        period = Period('1 month')

        specification = self.event_period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, LastMonthSpecification)

    def test_it_returns_last_day_specification(self) -> None:
        period = Period('24 hour')

        specification = self.event_period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, LastDaySpecification)

    def test_it_returns_empty_period_specification(self) -> None:
        period = Period('')

        specification = self.event_period_search.find_specification(period)

        self.assertIsInstance(specification, EmptyPeriodSpecification)

    def test_it_returns_date_range_specification(self) -> None:
        period = Period('')
        start_date = datetime.fromisoformat('2019-12-04')
        end_date = datetime.fromisoformat('2019-12-05')
        date_range = DateRange(start_date, end_date)
        date_range_specification = DateRangeSpecification(date_range)
        period_search = EventPeriodSearch([date_range_specification])
        specification = period_search.find_specification(period)

        self.assertEqual(specification.period(), str(period))
        self.assertIsInstance(specification, DateRangeSpecification)
