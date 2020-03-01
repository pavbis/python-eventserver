from typing import Iterator
from eventsserver.readmodel.results.abstract_result import AbstractResult


class SearchResult(AbstractResult):
    __results = iter([])

    def get_results(self) -> Iterator:
        return self.__results

    def set_results(self, results: Iterator) -> None:
        self.__results = results
