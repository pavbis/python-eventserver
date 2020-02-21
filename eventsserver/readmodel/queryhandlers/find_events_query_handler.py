from eventsserver.storage.read_event_stores import ProvidesEventStreams
from eventsserver.readmodel.queries.find_events_query import FindEventsQuery
from eventsserver.readmodel.results.find_events_result import FindEventsResult
from eventsserver.readmodel.constants.result_type import ResultType


class FindEventsQueryHandler(object):
    def __init__(self, event_store: ProvidesEventStreams):
        self.__event_store = event_store

    def handle(self, query: FindEventsQuery) -> FindEventsResult:
        try:
            events = self.__event_store.select_events(query)
            result = FindEventsResult()
            result.set_events(events)

            return result
        except Exception as error:
            return FindEventsResult(ResultType.FAILURE, str(error))
