from eventsserver.value.objects import ConsumerId, StreamName, EventName, MaxEventCount
from eventsserver.storage.read_event_stores import QueriesEvents


class FindEventsQuery(QueriesEvents):
    def __init__(
            self, consumer_id: ConsumerId, stream_name: StreamName,
            event_name: EventName, max_event_count: MaxEventCount
    ):
        self.__consumer_id = consumer_id
        self.__stream_name = stream_name
        self.__event_name = event_name
        self.__max_event_count = max_event_count

    def get_consumer_id(self) -> ConsumerId:
        return self.__consumer_id

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_event_name(self) -> EventName:
        return self.__event_name

    def get_max_event_count(self) -> MaxEventCount:
        return self.__max_event_count


