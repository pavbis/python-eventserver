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


class EventVersion(object):
    def __init__(self, primitive_value: int):
        if primitive_value < 1:
            raise InvalidArgument('Event version cannot be lower than 1.')
        self.__primitive_value = primitive_value

    def __int__(self):
        return self.__primitive_value


class SystemId(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('System ID cannot be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class SystemName(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('System name cannot be empty.')
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

        if 'event' not in event_data:
            raise InvalidArgument('Event JSON is missing an event section. This event should be considered broken.')

        if 'id' in event_data['event']:
            raise InvalidArgument('Event already has an event ID.')

        event_data['event']['id'] = str(event_id)

        return Event.from_event_data(event_data)


class Event(object):
    def __init__(self,
                 event_id: EventId, event_name: EventName, event_version: EventVersion,
                 system_id: SystemId, system_name: SystemName
                 ):
        self.__event_id = event_id
        self.__event_name = event_name
        self.__event_version = event_version
        self.__system_id = system_id
        self.__system_name = system_name

    def get_event_id(self) -> EventId:
        return self.__event_id

    def set_event_id(self, value) -> None:
        self.__event_id = value

    def get_event_name(self) -> EventName:
        return self.__event_name

    def set_event_name(self, value) -> None:
        self.__event_name = value

    def get_event_version(self) -> EventVersion:
        return self.__event_version

    def set_event_version(self, value) -> None:
        self.__event_version = value

    def get_system_id(self) -> SystemId:
        return self.__system_id

    def set_system_id(self, value) -> None:
        self.__system_id = value

    def get_system_name(self) -> SystemName:
        return self.__system_name

    def set_system_name(self, value) -> None:
        self.__system_name = value

    @classmethod
    def from_event_data(cls, event_data: dict):
        instance = cls.__new__(cls)

        instance.event_id = EventId(event_data['event']['id'])
        instance.event_name = EventName(event_data['event']['name'])
        instance.event_version = EventVersion(event_data['event']['version'])
        instance.system_id = SystemId(event_data['system']['id'])
        instance.system_name = SystemName(event_data['system']['name'])

        return instance

    event_id = property(get_event_id, set_event_id)
    event_name = property(get_event_name, set_event_name)
    event_version = property(get_event_version, set_event_version)
    system_id = property(get_system_id, set_system_id)
    system_name = property(get_system_name, set_system_name)
