from unittest import TestCase
from eventsserver.value.objects import SearchResult


class SearchResultTest(TestCase):
    def test_it_can_be_created_from_list(self) -> None:
        test_list = ['foo', 'bar', 'www']

        search_result = SearchResult.from_list(test_list)

        self.assertEqual(test_list[0], str(search_result.get_label()))
        self.assertEqual(test_list[1], str(search_result.get_category()))
        self.assertEqual(test_list[2], str(search_result.get_url()))
