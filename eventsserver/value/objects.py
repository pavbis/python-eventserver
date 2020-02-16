import uuid
import json


class InvalidArgument(ValueError):
    """Throw argument is not valid."""


class StreamName(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('stream name can not not be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class ProducerId(object):
    def __init__(self, primitive_value):
        try:
            uuid.UUID(str(primitive_value))
        except ValueError:
            raise InvalidArgument('invalid uuid provided.')
        self.__primitive_value = primitive_value

    def __eq__(self, other) -> bool:
        if not isinstance(other, ProducerId):
            return NotImplemented

        return self.__primitive_value == other.__primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class EventId(object):
    def __init__(self, primitive_value):
        try:
            uuid.UUID(str(primitive_value))
        except ValueError:
            raise InvalidArgument('invalid uuid provided.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class EventName(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('event name can not not be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class EventJson(object):
    def __init__(self, primitive_value: str):
        try:
            json.loads(primitive_value)
        except ValueError:
            raise InvalidArgument('Value is not a JSON string.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value

    def to_event_with_id(self, event_id: EventId):
        event_data = json.loads(self.__str__())
        print('event' not in event_data)
        if 'event' not in event_data:
            raise InvalidArgument('Event JSON is missing an event section. This event should be considered broken.')

        if 'id' in event_data['event']:
            raise InvalidArgument('Event already has an event ID.')

        event_data['event']['id'] = str(event_id)

        return event_data
