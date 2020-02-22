from eventsserver.value.objects import (
    ProducerId, StreamName, EventCount, ConsumerCount, OccurredOn
)


class StreamData:
    __producer_id = None
    __stream_name = None
    __events_count = None
    __consumer_count = None
    __first_event_occurred_at = None
    __last_event_occurred_at = None

    @classmethod
    def from_list(cls, stream_data: []):
        instance = cls.__new__(cls)

        instance.__producer_id = ProducerId(stream_data[0])
        instance.__stream_name = StreamName(stream_data[1])
        instance.__events_count = EventCount(stream_data[2])
        instance.__consumer_count = ConsumerCount(stream_data[3])
        instance.__first_event_occurred_at = OccurredOn(stream_data[4])
        instance.__last_event_occurred_at = OccurredOn(stream_data[5])

        return instance

    def get_producer_id(self) -> ProducerId:
        return self.__producer_id

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_events_count(self) -> EventCount:
        return self.__events_count

    def get_consumer_count(self) -> ConsumerCount:
        return self.__consumer_count

    def get_first_event_occurred_at(self) -> OccurredOn:
        return self.__first_event_occurred_at

    def get_last_event_occurred_at(self) -> OccurredOn:
        return self.__last_event_occurred_at
