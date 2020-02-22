from eventsserver.storage.write_event_stores import PersistsEventStreams
from eventsserver.writemodel.commands.receive_event_command import ReceiveEventCommand
from eventsserver.writemodel.results.receive_event_result import ReceiveEventResult
from eventsserver.writemodel.constants.result_type import ResultType


class ReceiveEventCommandHandler:
    def __init__(self, event_store: PersistsEventStreams):
        self.__event_store = event_store

    def handle(self, command: ReceiveEventCommand) -> ReceiveEventResult:
        try:
            event_id = command.get_event_id()
            event = command.get_event_json().to_event_with_id(event_id)
            self.__event_store.record_event(command.get_producer_id(), command.get_stream_name(), event)

            result = ReceiveEventResult()
            result.set_event_id(event_id)

            return result
        except Exception as error:
            return ReceiveEventResult(ResultType.FAILURE, str(error))
