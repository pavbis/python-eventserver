from unittest import TestCase
from tests.unit.fakes.storage.in_memory_search_results_storage import InMemorySearchResultsStorage
from eventsserver.readmodel.queryhandlers.autocomplete_results_query_handler import AutoCompleteResultsQueryHandler
from eventsserver.readmodel.results.auto_complete_result import AutoCompleteResult
from eventsserver.readmodel.queries.search_query import SearchQuery
from eventsserver.value.objects import SearchTerm


class AutoCompleteResultsQueryHandlerTest(TestCase):
    def setUp(self) -> None:
        self.storage = InMemorySearchResultsStorage()
        self.storage.reset()
        self.query_handler = AutoCompleteResultsQueryHandler(self.storage)

    def test_it_returns_success_result(self) -> None:
        result = self.__handle_query()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual('{"foo": "bar"}', str(result.get_aggregated_json()))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.storage.will_raise_database_error()

        result = self.__handle_query()

        self.assertTrue(result.failure())
        self.assertEqual(self.storage.SEARCH_AUTOCOMPLETE_RESULTS_STORAGE_ERROR, result.get_message())

    def __handle_query(self) -> AutoCompleteResult:
        query = SearchQuery(SearchTerm('test'))

        return self.query_handler.handle(query)
