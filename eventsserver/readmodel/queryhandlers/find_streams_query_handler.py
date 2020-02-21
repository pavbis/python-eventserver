from eventsserver.storage.read_event_stores import ProvidesEventStreams
from eventsserver.readmodel.queries.find_streams_query import FindStreamsQuery
from eventsserver.readmodel.results.find_streams_result import FindStreamsResult
from eventsserver.readmodel.constants.result_type import ResultType


class FindStreamsQueryHandler(object):
    def __init__(self, event_store: ProvidesEventStreams):
        self.__even_store = event_store

    def handle(self, query: FindStreamsQuery) -> FindStreamsResult:
        try:
            events = self.__even_store.select_streams(query.get_expression())
            result = FindStreamsResult()
            result.set_events(events)

            return result
        except Exception as error:
            return FindStreamsResult(ResultType.FAILURE, str(error))
