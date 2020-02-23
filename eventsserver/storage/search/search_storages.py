from typing import Iterator
from pg8000 import Connection, PGJson
from eventsserver.value.objects import ProvidesAggregatedJson, SearchTerm, AggregatedJson, EmptyJson, SearchResult


class ProvidesSearchResults:
    def autocomplete_list(self, search_tern: SearchTerm) -> ProvidesAggregatedJson:
        raise NotImplementedError

    def search_results(self, search_term: SearchTerm) -> Iterator[SearchResult]:
        raise NotImplementedError


class PosgreSqlSearchResultsStorage(ProvidesSearchResults):
    def __init__(self, connection: Connection):
        self.__connection = connection

    def autocomplete_list(self, search_tern: SearchTerm) -> ProvidesAggregatedJson:
        with self.__connection.cursor() as cursor:
            query = 'SELECT json_agg(row_to_json(searchResults)) FROM (SELECT * FROM search_result(%s)) searchResults'

            cursor.execute(query, [str(search_tern)])
            row = cursor.fetchone()

            if row is None:
                return EmptyJson()
            else:
                return AggregatedJson(row[0])

    def search_results(self, search_term: SearchTerm) -> Iterator[SearchResult]:
        with self.__connection.cursor() as cursor:
            query = 'SELECT * FROM search_result(%s)'

            cursor.execute(query, [str(search_term)])
            rows = cursor.fetchall()

            for row in rows:
                yield SearchResult.from_list(row)
