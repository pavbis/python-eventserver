from eventsserver.value.objects import EventId, EventName


class Event(object):
    def __init__(self, event_id: EventId, event_name: EventName):
        self.__event_id = event_id
        self.__event_name = event_name

    def get_event_id(self):
        return self.__event_id

    def set_event_id(self, value):
        self.__event_id = value

    def get_event_name(self):
        return self.__event_name

    def set_event_name(self, value):
        self.__event_name = value

    event_id = property(get_event_id, set_event_id)
    event_name = property(get_event_name, set_event_name)
