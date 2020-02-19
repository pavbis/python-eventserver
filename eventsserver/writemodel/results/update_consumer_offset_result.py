from eventsserver.writemodel.results.abstract_result import AbstractResult
from eventsserver.value.objects import Offset, EventName, ConsumerId


class UpdateConsumerOffsetResult(AbstractResult):
    __offset = None
    __event_name = None
    __consumer_id = None

    def get_offset(self) -> Offset:
        return self.__offset

    def set_offset(self, offset: Offset) -> None:
        self.__offset = offset

    def get_event_name(self) -> EventName:
        return self.__event_name

    def set_event_name(self, event_name: EventName) -> None:
        self.__event_name = event_name

    def get_consumer_id(self) -> ConsumerId:
        return self.__consumer_id

    def set_consumer_id(self, consumer_id: ConsumerId) -> None:
        self.__consumer_id = consumer_id
