from unittest import TestCase
from tests.unit.fakes.storage.in_memory_statistics_storage import InMemoryStatisticsStorage
from eventsserver.readmodel.queryhandlers.read_statistics_query_handler import ReadStatisticsDataQueryHandler


class ReadStatisticsQueryHandlerTest(TestCase):
    def setUp(self) -> None:
        self.storage = InMemoryStatisticsStorage()
        self.storage.reset()
        self.query_handler = ReadStatisticsDataQueryHandler(self.storage)

    def test_it_returns_success_result(self) -> None:
        result = self.query_handler.handle()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual('{"foo": "bar"}', str(result.get_event_chart_data()))
        self.assertEqual('{"foo": "bar"}', str(result.get_stream_chart_data()))
        self.assertEqual('{"foo": "bar"}', str(result.get_stream_statistics_chart_data()))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.storage.will_raise_database_error()

        result = self.query_handler.handle()

        self.assertTrue(result.failure())
        self.assertEqual(self.storage.STATISTICS_STORAGE_ERROR, result.get_message())
