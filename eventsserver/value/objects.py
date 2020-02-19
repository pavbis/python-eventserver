import uuid
import json
import pytz
from datetime import datetime


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


class TimeZone(object):
    def __init__(self, primitive_value: str):
        if primitive_value not in pytz.all_timezones:
            raise InvalidArgument('Unknown or bad timezone.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class TriggerType(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('Trigger type cannot be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class TriggerName(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('Trigger name cannot be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class PayLoad(object):
    def __init__(self, primitive_value: dict):
        if not isinstance(primitive_value, dict):
            raise InvalidArgument('Payload must be an dict.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return str(self.__primitive_value)


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


class ConsumerId(object):
    def __init__(self, primitive_value):
        try:
            uuid.UUID(str(primitive_value))
        except ValueError:
            raise InvalidArgument('invalid uuid provided.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class Offset(object):
    def __init__(self, primitive_value: int):
        if primitive_value < 0:
            raise InvalidArgument('Offset cannot be lower than zero.')
        self.__primitive_value = primitive_value

    def __int__(self):
        return self.__primitive_value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Offset):
            return NotImplemented
        return self.__primitive_value == other.__primitive_value

    def increment(self):
        self.__primitive_value += 1

        return self


class EventCount(object):
    def __init__(self, primitive_value: int):
        if primitive_value < 0:
            raise InvalidArgument('Event count cannot be lower than zero.')
        self.__primitive_value = primitive_value

    def __int__(self):
        return self.__primitive_value


class MaxEventCount(object):
    def __init__(self, primitive_value: int):
        if primitive_value < 1:
            raise InvalidArgument('Max consume count must be greater than 0.')
        self.__primitive_value = primitive_value

    def __int__(self):
        return self.__primitive_value


class ConsumerCount(object):
    def __init__(self, primitive_value: int):
        if primitive_value < 0:
            raise InvalidArgument('Consumer count cannot be lower than zero.')
        self.__primitive_value = primitive_value

    def __int__(self):
        return self.__primitive_value


class OccurredOn(object):
    def __init__(self, primitive_value: int):
        self.__primitive_value = primitive_value

    def __int__(self):
        return self.__primitive_value


class Event(object):
    def __init__(self,
                 event_id: EventId, event_name: EventName, event_version: EventVersion,
                 system_id: SystemId, system_name: SystemName, time_zone: TimeZone,
                 system_time: datetime, trigger_type: TriggerType, trigger_name: TriggerName, payload: PayLoad
                 ):
        self.__event_id = event_id
        self.__event_name = event_name
        self.__event_version = event_version
        self.__system_id = system_id
        self.__system_name = system_name
        self.__time_zone = time_zone
        self.__system_time = system_time
        self.__trigger_type = trigger_type
        self.__trigger_name = trigger_name
        self.__payload = payload

    def get_event_id(self) -> EventId:
        return self.__event_id

    def get_event_name(self) -> EventName:
        return self.__event_name

    def get_event_version(self) -> EventVersion:
        return self.__event_version

    def get_system_id(self) -> SystemId:
        return self.__system_id

    def get_system_name(self) -> SystemName:
        return self.__system_name

    def get_time_zone(self) -> TimeZone:
        return self.__time_zone

    def get_system_time(self) -> datetime:
        return self.__system_time

    def get_trigger_type(self) -> TriggerType:
        return self.__trigger_type

    def get_trigger_name(self) -> TriggerName:
        return self.__trigger_name

    def get_payload(self) -> PayLoad:
        return self.__payload

    @classmethod
    def from_event_data(cls, event_data: dict):
        instance = cls.__new__(cls)

        instance.__event_id = EventId(event_data['event']['id'])
        instance.__event_name = EventName(event_data['event']['name'])
        instance.__event_version = EventVersion(event_data['event']['version'])
        instance.__system_id = SystemId(event_data['system']['id'])
        instance.__system_name = SystemName(event_data['system']['name'])
        instance.__time_zone = TimeZone(event_data['system']['timezone'])
        instance.__system_time = datetime.fromisoformat(event_data['system']['time'])
        instance.__trigger_type = TriggerType(event_data['trigger']['type'])
        instance.__trigger_name = TriggerName(event_data['trigger']['name'])
        instance.__payload = PayLoad(event_data['payload'])

        return instance

    def to_event_data(self) -> dict:
        event_data = {'event': {}, 'system': {}, 'trigger': {}, 'payload': {str(self.__payload)}}

        event_data['event']['id'] = str(self.__event_id)
        event_data['event']['name'] = str(self.__event_name)
        event_data['event']['version'] = int(self.__event_version)
        event_data['system']['id'] = str(self.__system_id)
        event_data['system']['name'] = str(self.__system_name)
        event_data['system']['time'] = str(self.__system_time)
        event_data['system']['timezone'] = str(self.__time_zone)
        event_data['trigger']['name'] = str(self.__trigger_name)
        event_data['trigger']['type'] = str(self.__trigger_type)

        return event_data

    def to_json(self) -> str:
        return json.dumps(self.to_event_data(), cls=SetEncoder)

    event_id = property(get_event_id)
    event_name = property(get_event_name)
    event_version = property(get_event_version)
    system_id = property(get_system_id)
    system_name = property(get_system_name)
    time_zone = property(get_time_zone)
    system_time = property(get_system_time)
    trigger_type = property(get_trigger_type)
    trigger_name = property(get_trigger_name)
    payload = property(get_payload)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
