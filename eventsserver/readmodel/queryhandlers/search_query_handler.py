from eventsserver.storage.search.search_storages import ProvidesSearchResults
from eventsserver.readmodel.queries.search_query import SearchQuery
from eventsserver.readmodel.results.search_result import SearchResult
from eventsserver.readmodel.constants.result_type import ResultType


class SearchResultsQueryHandler:
    def __init__(self, storage: ProvidesSearchResults):
        self.__storage = storage

    def handle(self, query: SearchQuery) -> SearchResult:
        try:
            search_results = self.__storage.search_results(query.get_search_term())

            result = SearchResult()
            result.set_results(search_results)

            return result
        except Exception as error:
            return SearchResult(ResultType.FAILURE, str(error))
