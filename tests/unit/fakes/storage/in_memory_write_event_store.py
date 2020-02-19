from eventsserver.storage.write_event_stores import PersistsEventStreams
from eventsserver.value.objects import StreamName, ConsumerId, EventName, Offset, EventId, ProducerId, Event
from pg8000 import DatabaseError


class InMemoryWriteEventStore(PersistsEventStreams):
    EVENT_STORE_RECORD_EVENT_ERROR = 'record event failed'
    EVENT_STORE_ACKNOWLEDGE_EVENT_ERROR = 'acknowledge event failed'
    EVENT_STORE_UPDATE_CONSUMER_OFFSET_ERROR = 'update consumer offset failed'

    events = {}
    __will_raise_database_error = False

    def will_raise_database_error(self):
        self.__will_raise_database_error = True

    def reset(self):
        self.__will_raise_database_error = False

    def record_event(self, producer_id: ProducerId, stream_name: StreamName, event: Event) -> None:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_RECORD_EVENT_ERROR)

        self.events[str(producer_id)] = event

    def acknowledge_event(self, consumer_id: ConsumerId, stream_name: StreamName, event_id: EventId) -> None:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_ACKNOWLEDGE_EVENT_ERROR)

    def update_consumer_offset(self, stream_name: StreamName, consumer_id: ConsumerId, event_name: EventName,
                               offset: Offset) -> None:
        if self.__will_raise_database_error:
            raise DatabaseError(self.EVENT_STORE_UPDATE_CONSUMER_OFFSET_ERROR)
