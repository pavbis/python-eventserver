from eventsserver.value.objects import (
    ConsumerId, EventName, Offset, OccurredOn, ConsumedPercentage, Behind
)


class ConsumerData(object):
    __consumer_id = None
    __event_name = None
    __offset = None
    __moved_at = None
    __consumed_percentage = None
    __behind = None

    @classmethod
    def from_list(cls, consumer_data: []):
        instance = cls.__new__(cls)

        instance.__consumer_id = ConsumerId(consumer_data[0])
        instance.__offset = Offset(consumer_data[1])
        instance.__moved_at = OccurredOn(consumer_data[2])
        instance.__event_name = EventName(consumer_data[3])
        instance.__consumed_percentage = ConsumedPercentage(consumer_data[4])
        instance.__behind = Behind(consumer_data[5])

        return instance

    def get_consumer_id(self) -> ConsumerId:
        return self.__consumer_id

    def get_event_name(self) -> EventName:
        return self.__event_name

    def get_offset(self) -> Offset:
        return self.__offset

    def get_moved_at(self) -> OccurredOn:
        return self.__moved_at

    def get_consumed_percentage(self) -> ConsumedPercentage:
        return self.__consumed_percentage

    def get_behind(self) -> Behind:
        return self.__behind
