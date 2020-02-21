from eventsserver.readmodel.results.abstract_result import AbstractResult
from typing import Iterator


class FindConsumersResult(AbstractResult):
    __consumers = iter([])

    def get_consumers(self) -> Iterator:
        return self.__consumers

    def set_consumers(self, consumers: Iterator) -> None:
        self.__consumers = consumers
