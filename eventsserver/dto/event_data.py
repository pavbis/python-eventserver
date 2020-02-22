from eventsserver.value.objects import (
    ConsumerId, EventName, EventId, OccurredOn
)


class EventData:
    __event_name = None
    __created_at = None
    __consumer_ids = []
    __event_id = None

    @classmethod
    def from_list(cls, event_data: []):
        instance = cls.__new__(cls)

        instance.__event_name = EventName(event_data[0])
        instance.__created_at = OccurredOn(event_data[1])

        if event_data[2] is not None:
            split_consumer_ids = event_data[2].split(',')

            for primitive_consumer_id in split_consumer_ids:
                instance.__consumer_ids.append(ConsumerId(primitive_consumer_id.strip()))
        else:
            instance.__consumer_ids = []

        instance.__event_id = EventId(event_data[3])

        return instance

    def get_consumer_ids(self) -> [ConsumerId]:
        return self.__consumer_ids

    def get_event_name(self) -> EventName:
        return self.__event_name

    def get_created_at(self) -> OccurredOn:
        return self.__created_at

    def get_event_id(self) -> EventId:
        return self.__event_id
