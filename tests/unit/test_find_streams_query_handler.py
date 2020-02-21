from unittest import TestCase
from tests.unit.fakes.storage.in_memory_read_event_store import InMemoryReadEventStore
from eventsserver.readmodel.queryhandlers.find_streams_query_handler import FindStreamsQueryHandler
from eventsserver.readmodel.queries.find_streams_query import FindStreamsQuery
from eventsserver.storage.expressions.select_streams_expressions import ProducerIdExpression
from eventsserver.storage.expressions.select_streams_expressions import SearchArgument

from eventsserver.readmodel.results.find_streams_result import FindStreamsResult


class FindStreamsQueryHandlerTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryReadEventStore()
        self.event_store.reset()
        self.query_handler = FindStreamsQueryHandler(event_store=self.event_store)

    def test_it_returns_success_result(self) -> None:
        result = self.__handle_query()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(1, sum(1 for _ in result.get_streams()))

    def test_it_returns_failure_if_event_store_exception_raised(self) -> None:
        self.event_store.will_raise_database_error()

        result = self.__handle_query()

        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_SELECT_STREAMS_ERROR, result.get_message())
        self.assertEqual(0, sum(1 for _ in result.get_streams()))

    def __handle_query(self) -> FindStreamsResult:
        expression = ProducerIdExpression(SearchArgument('f1f5cae6-30b7-43e7-a5e8-746a98bc265e'))
        query = FindStreamsQuery(expression)

        return self.query_handler.handle(query)
