from pg8000 import DatabaseError
from typing import Iterator
from eventsserver.dto.consumer_data import ConsumerData
from eventsserver.dto.event_data import EventData
from eventsserver.dto.stream_data import StreamData
from eventsserver.storage.read_event_stores import ProvidesEventStreams, SpecifiesPeriod, ProvidesPredicate, \
    QueriesEvents
from eventsserver.value.objects import EventId, EventJson, StreamName
from eventsserver.value.objects import Event


class InMemoryReadEventStore(ProvidesEventStreams):
    EVENT_STORE_SELECT_EVENTS_ERROR = 'select events failed'
    EVENT_STORE_SELECT_STREAMS_ERROR = 'select streams failed'
    EVENT_STORE_SELECT_CONSUMERS_ERROR = 'select consumers failed'
    EVENT_STORE_READ_EVENT_PAYLOAD_ERROR = 'read event payload failed'
    EVENT_PAYLOAD = '{"event": {"id": "ebf1e616-ca51-4f76-908d-d5781c0ad550", "name": "Snickers", "version": 1}, ' \
                    '"system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", "timezone": ' \
                    '"Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", "type": "system"}} '

    __will_raise_database_error = False

    def will_raise_database_error(self) -> None:
        self.__will_raise_database_error = True

    def reset(self):
        self.__will_raise_database_error = False

    def select_events(self, query: QueriesEvents) -> Iterator[Event]:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_SELECT_EVENTS_ERROR)

        return iter([Event.from_event_data({'event': {'name': 'Snickers', 'version': 1, 'id': 'c3f390b8-302f-49af-b987'
                                                                                              '-66ab0a931a62'},
                                            'system': {'id': 'alv1', 'name': 'codello alvine',
                                                       'time': '2019-09-06 13:58:12',
                                                       'timezone': 'Europe/Berlin'},
                                            'payload': {'foo': 'bar'},
                                            'trigger': {'name': '/path/to/script.php', 'type': 'system'}})])

    def select_streams(self, expression: ProvidesPredicate) -> Iterator[StreamData]:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_SELECT_STREAMS_ERROR)

        return iter([StreamData.from_list([
            'c3f390b8-302f-49af-b987-66ab0a931a62', 'unit-test', 1,
            2, '2019-11-08 08:38:35.806000+00:00', '2019-11-26 09:02:29.418000+00:00'
        ])])

    def select_consumers_for_stream(self, stream_name: StreamName) -> Iterator[ConsumerData]:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_SELECT_CONSUMERS_ERROR)

        return iter([ConsumerData.from_list(
            ['c3f390b8-302f-49af-b987-66ab0a931a62', 1, '2019-11-08 08:38:35.806000+00:00', 'unit-test', 55.5, 12]
        )])

    def select_events_for_stream(self, stream_name: StreamName, period: SpecifiesPeriod,
                                 expression: ProvidesPredicate) -> Iterator[EventData]:
        pass

    def read_payload_for_event_id(self, event_id: EventId) -> EventJson:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_READ_EVENT_PAYLOAD_ERROR)

        return EventJson(self.EVENT_PAYLOAD)
