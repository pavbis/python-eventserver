from typing import Iterator
from pg8000 import DatabaseError
from eventsserver.storage.search.search_storages import ProvidesSearchResults
from eventsserver.value.objects import SearchTerm, SearchResult, ProvidesAggregatedJson, AggregatedJson


class InMemorySearchResultsStorage(ProvidesSearchResults):
    SEARCH_RESULTS_STORAGE_ERROR = 'search results error'
    SEARCH_AUTOCOMPLETE_RESULTS_STORAGE_ERROR = 'auto complete results error'

    __will_raise_database_error = False

    def will_raise_database_error(self) -> None:
        self.__will_raise_database_error = True

    def reset(self):
        self.__will_raise_database_error = False

    def autocomplete_list(self, search_tern: SearchTerm) -> ProvidesAggregatedJson:
        if self.__will_raise_database_error:
            raise DatabaseError(self.SEARCH_AUTOCOMPLETE_RESULTS_STORAGE_ERROR)

        return AggregatedJson('{"foo": "bar"}')

    def search_results(self, search_term: SearchTerm) -> Iterator[SearchResult]:
        if self.__will_raise_database_error:
            raise DatabaseError(self.SEARCH_RESULTS_STORAGE_ERROR)

        return iter([SearchResult.from_list(['foo', 'bar', 'www'])])
