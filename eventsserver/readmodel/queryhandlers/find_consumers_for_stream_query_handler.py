from eventsserver.storage.read_event_stores import ProvidesEventStreams
from eventsserver.readmodel.queries.find_consumers_query import FindConsumersQuery
from eventsserver.readmodel.results.find_consumers_result import FindConsumersResult
from eventsserver.readmodel.constants.result_type import ResultType


class FindConsumersForStreamQueryHandler:
    def __init__(self, event_store: ProvidesEventStreams):
        self.__event_store = event_store

    def handle(self, query: FindConsumersQuery) -> FindConsumersResult:
        try:
            consumers = self.__event_store.select_consumers_for_stream(query.get_stream_name())
            result = FindConsumersResult()
            result.set_consumers(consumers)

            return result
        except Exception as error:
            return FindConsumersResult(ResultType.FAILURE, str(error))
