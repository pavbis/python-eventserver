from eventsserver.storage.read_event_stores import ProvidesEventStreams
from eventsserver.readmodel.queries.read_event_payload_query import ReadEventPayloadQuery
from eventsserver.readmodel.results.read_event_payload_result import ReadEventPayloadResult
from eventsserver.readmodel.constants.result_type import ResultType


class ReadEventPayloadQueryHandler(object):
    def __init__(self, event_store: ProvidesEventStreams):
        self.__event_store = event_store

    def handle(self, query: ReadEventPayloadQuery) -> ReadEventPayloadResult:
        try:
            event_payload = self.__event_store.read_payload_for_event_id(query.get_event_id())

            result = ReadEventPayloadResult()
            result.set_event_json(event_payload)

            return result
        except Exception as error:
            return ReadEventPayloadResult(ResultType.FAILURE, str(error))
