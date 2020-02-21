from eventsserver.readmodel.results.abstract_result import AbstractResult
from typing import Iterator


class FindStreamsResult(AbstractResult):
    __streams = iter([])

    def get_streams(self) -> Iterator:
        return self.__streams

    def set_events(self, streams: Iterator) -> None:
        self.__streams = streams
