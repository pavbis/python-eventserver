from unittest import TestCase
from tests.unit.fakes.storage.in_memory_read_event_store import InMemoryReadEventStore
from eventsserver.readmodel.queryhandlers.find_consumers_for_stream_query_handler import FindConsumersForStreamQueryHandler
from eventsserver.value.objects import StreamName
from eventsserver.readmodel.results.find_consumers_result import FindConsumersResult
from eventsserver.readmodel.queries.find_consumers_query import FindConsumersQuery


class FindConsumersForStreamTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryReadEventStore()
        self.event_store.reset()
        self.query_handler = FindConsumersForStreamQueryHandler(event_store=self.event_store)

    def test_it_returns_success_result(self) -> None:
        result = self.__handle_query()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(1, sum(1 for _ in result.get_consumers()))

    def test_it_returns_failure_if_event_store_exception_raised(self) -> None:
        self.event_store.will_raise_database_error()
        result = self.__handle_query()

        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_SELECT_CONSUMERS_ERROR, str(result.get_message()))

    def __handle_query(self) -> FindConsumersResult:

        query = FindConsumersQuery(StreamName('test'))

        return self.query_handler.handle(query)
