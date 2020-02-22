from eventsserver.value.objects import ConsumerId, StreamName, EventId


class ReceiveAcknowledgementCommand:
    def __init__(self, consumer_id: ConsumerId, stream_name: StreamName, event_id: EventId):
        self.__consumer_id = consumer_id
        self.__stream_name = stream_name
        self.__event_id = event_id

    def get_consumer_id(self) -> ConsumerId:
        return self.__consumer_id

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_event_id(self) -> EventId:
        return self.__event_id
