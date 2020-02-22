from eventsserver.value.objects import EventId, ProducerId, StreamName, EventJson


class ReceiveEventCommand:
    def __init__(self, event_id: EventId, producer_id: ProducerId, stream_name: StreamName, event_json: EventJson):
        self.__event_id = event_id
        self.__producer_id = producer_id
        self.__stream_name = stream_name
        self.__event_json = event_json

    def get_event_id(self) -> EventId:
        return self.__event_id

    def get_producer_id(self) -> ProducerId:
        return self.__producer_id

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

    def get_event_json(self) -> EventJson:
        return self.__event_json
