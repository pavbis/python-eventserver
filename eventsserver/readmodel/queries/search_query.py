from eventsserver.value.objects import SearchTerm


class SearchQuery:
    def __init__(self, search_term: SearchTerm):
        self.__search_term = search_term

    def get_search_term(self) -> SearchTerm:
        return self.__search_term
