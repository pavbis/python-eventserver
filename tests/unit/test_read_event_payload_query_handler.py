from unittest import TestCase
from tests.unit.fakes.storage.in_memory_read_event_store import InMemoryReadEventStore
from eventsserver.readmodel.queries.read_event_payload_query import ReadEventPayloadQuery
from eventsserver.readmodel.queryhandlers.read_event_payload_query_handler import ReadEventPayloadQueryHandler
from eventsserver.value.objects import EventId
from eventsserver.readmodel.results.read_event_payload_result import ReadEventPayloadResult


class ReadEventPayloadQueryHandlerTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryReadEventStore()
        self.event_store.reset()
        self.query_handler = ReadEventPayloadQueryHandler(self.event_store)

    def test_it_returns_success_result(self) -> None:
        result = self.__handle_query()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(self.event_store.EVENT_PAYLOAD, str(result.get_event_json()))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.event_store.will_raise_database_error()

        result = self.__handle_query()

        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_READ_EVENT_PAYLOAD_ERROR, result.get_message())

    def __handle_query(self) -> ReadEventPayloadResult:

        event_id = EventId('ebf1e616-ca51-4f76-908d-d5781c0ad550')
        query = ReadEventPayloadQuery(event_id)

        return self.query_handler.handle(query)
