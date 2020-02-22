from eventsserver.value.objects import EventJson
from eventsserver.readmodel.results.abstract_result import AbstractResult


class ReadEventPayloadResult(AbstractResult):
    __event_json = None

    def get_event_json(self) -> EventJson:
        return self.__event_json

    def set_event_json(self, event_json: EventJson) -> None:
        self.__event_json = event_json