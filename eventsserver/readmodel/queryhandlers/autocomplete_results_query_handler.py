from eventsserver.storage.search.search_storages import ProvidesSearchResults
from eventsserver.readmodel.queries.search_query import SearchQuery
from eventsserver.readmodel.results.auto_complete_result import AutoCompleteResult
from eventsserver.readmodel.constants.result_type import ResultType


class AutoCompleteResultsQueryHandler:
    def __init__(self, storage: ProvidesSearchResults):
        self.__storage = storage

    def handle(self, query: SearchQuery) -> AutoCompleteResult:
        try:
            autocomplete_result = self.__storage.autocomplete_list(query.get_search_term())

            result = AutoCompleteResult()
            result.set_aggregated_json(autocomplete_result)

            return result
        except Exception as error:
            return AutoCompleteResult(ResultType.FAILURE, str(error))
