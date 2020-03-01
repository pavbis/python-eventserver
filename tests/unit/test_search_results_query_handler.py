from unittest import TestCase
from tests.unit.fakes.storage.in_memory_search_results_storage import InMemorySearchResultsStorage
from eventsserver.readmodel.queryhandlers.search_query_handler import SearchResultsQueryHandler
from eventsserver.readmodel.results.search_result import SearchResult
from eventsserver.readmodel.queries.search_query import SearchQuery
from eventsserver.value.objects import SearchTerm


class SearchResultsQueryHandlerTest(TestCase):
    def setUp(self) -> None:
        self.storage = InMemorySearchResultsStorage()
        self.storage.reset()
        self.query_handler = SearchResultsQueryHandler(self.storage)

    def test_it_returns_success_result(self) -> None:
        result = self.__handle_query()

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(1, sum(1 for _ in result.get_results()))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.storage.will_raise_database_error()

        result = self.__handle_query()

        self.assertTrue(result.failure())
        self.assertEqual(self.storage.SEARCH_RESULTS_STORAGE_ERROR, result.get_message())

    def __handle_query(self) -> SearchResult:
        query = SearchQuery(SearchTerm('test'))

        return self.query_handler.handle(query)
