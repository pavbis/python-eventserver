from eventsserver.readmodel.results.abstract_result import AbstractResult
from typing import Iterator


class FindEventsResult(AbstractResult):
    __events = None

    def get_events(self) -> Iterator:
        return self.__events

    def set_events(self, events: Iterator) -> None:
        self.__events = events
