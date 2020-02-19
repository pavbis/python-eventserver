from eventsserver.writemodel.results.abstract_result import AbstractResult
from eventsserver.value.objects import EventId


class ReceiveAcknowledgementResult(AbstractResult):
    __event_id = None

    def get_event_id(self) -> EventId:
        return self.__event_id

    def set_event_id(self, event_id: EventId) -> None:
        self.__event_id = event_id
