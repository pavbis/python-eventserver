from eventsserver.value.objects import EventId


class ReadEventPayloadQuery(object):
    def __init__(self, event_id: EventId):
        self.__event_id = event_id

    def get_event_id(self) -> EventId:
        return self.__event_id
