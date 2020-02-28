from eventsserver.value.objects import (
    InvalidArgument, StreamName, ProducerId, EventCount, ConsumerCount, ConsumerId, Offset, EventName
)


class StreamCount:
    def __init__(self, primitive_value: int):
        if primitive_value < 0:
            raise InvalidArgument('Stream count cannot be lower than zero.')
        self.__primitive_value = primitive_value

    def __int__(self) -> int:
        return self.__primitive_value


class StreamTotals:
    __stream_name = None
    __producer_id = None
    __events = None

    @classmethod
    def from_list(cls, stream_totals_data: []):
        instance = cls.__new__(cls)

        instance.__stream_name = StreamName(stream_totals_data[0])
        instance.__producer_id = ProducerId(stream_totals_data[1])
        instance.__events = EventCount(stream_totals_data[2])

        return instance

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_producer_id(self) -> ProducerId:
        return self.__producer_id

    def get_events(self) -> EventCount:
        return self.__events


class ConsumerTotals:
    __stream_name = None
    __consumers_count = None

    @classmethod
    def from_list(cls, consumer_totals_data: []):
        instance = cls.__new__(cls)

        instance.__stream_name = StreamName(consumer_totals_data[0])
        instance.__consumers_count = ConsumerCount(consumer_totals_data[1])

        return instance

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_consumers_count(self) -> ConsumerCount:
        return self.__consumers_count


class ConsumerOffset:
    __stream_name = None
    __consumer_id = None
    __offset = None
    __event_name = None

    @classmethod
    def from_list(cls, consumer_offset_data: []):
        instance = cls.__new__(cls)

        instance.__consumer_id = ConsumerId(consumer_offset_data[0])
        instance.__stream_name = StreamName(consumer_offset_data[1])
        instance.__offset = Offset(consumer_offset_data[2])
        instance.__event_name = EventName(consumer_offset_data[3])

        return instance

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_consumer_id(self) -> ConsumerId:
        return self.__consumer_id

    def get_offset(self) -> Offset:
        return self.__offset

    def get_event_name(self) -> EventName:
        return self.__event_name
