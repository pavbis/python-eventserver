from unittest import TestCase
from eventsserver.readmodel.results.find_events_result import FindEventsResult
from eventsserver.readmodel.queryhandlers.find_events_query_handler import FindEventsQueryHandler
from tests.unit.fakes.storage.in_memory_read_event_store import InMemoryReadEventStore
from eventsserver.readmodel.queries.find_events_query import FindEventsQuery
from eventsserver.value.objects import ConsumerId, StreamName, EventName, MaxEventCount
import uuid


class FindEventsQueryHandlerTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryReadEventStore()
        self.event_store.reset()
        self.query_handler = FindEventsQueryHandler(event_store=self.event_store)

    def test_it_returns_success_result(self) -> None:
        result = self.__handle_query()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(1, sum(1 for _ in result.get_events()))

    def test_it_returns_failure_if_event_store_exception_raised(self) -> None:
        self.event_store.will_raise_database_error()
        result = self.__handle_query()

        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_SELECT_EVENTS_ERROR, str(result.get_message()))

    def __handle_query(self) -> FindEventsResult:
        query = FindEventsQuery(
            consumer_id=ConsumerId(str(uuid.uuid4())),
            stream_name=StreamName('test'),
            event_name=EventName('foo'),
            max_event_count=MaxEventCount(100)
        )

        return self.query_handler.handle(query)
