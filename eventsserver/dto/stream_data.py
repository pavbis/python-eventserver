from eventsserver.value.objects import (
    ProducerId, StreamName, EventCount, ConsumerCount, OccurredOn
)


class StreamData(object):
    __producer_id = None
    __stream_name = None
    __events_count = None
    __consumer_count = None
    __first_event_occurred_at = None
    __last_event_occurred_at = None

    @classmethod
    def from_dict(cls, stream_data: dict):
        instance = cls.__new__(cls)

        instance.__producer_id = ProducerId(stream_data['producer_id'])
        instance.__stream_name = StreamName(stream_data['stream_name'])
        instance.__events_count = EventCount(stream_data['events_count'])
        instance.__consumer_count = ConsumerCount(stream_data['consumer_count'])
        instance.__first_event_occurred_at = OccurredOn(stream_data['first_event_occurred_at'])
        instance.__last_event_occurred_at = OccurredOn(stream_data['last_event_occurred_at'])

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
