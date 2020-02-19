from eventsserver.value.objects import ConsumerId, StreamName, EventName, Offset


class UpdateConsumerOffsetCommand(object):
    def __init__(self, consumer_id: ConsumerId, stream_name: StreamName, event_name: EventName, offset: Offset):
        self.__consumer_id = consumer_id
        self.__stream_name = stream_name
        self.__event_name = event_name
        self.__offset = offset

    def get_consumer_id(self) -> ConsumerId:
        return self.__consumer_id

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_event_name(self) -> EventName:
        return self.__event_name

    def get_offset(self) -> Offset:
        return self.__offset
