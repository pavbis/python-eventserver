from eventsserver.storage.write_event_stores import PersistsEventStreams
from eventsserver.writemodel.commands.receive_acknowledgement_command import ReceiveAcknowledgementCommand
from eventsserver.writemodel.results.receive_acknowledgement_result import ReceiveAcknowledgementResult
from eventsserver.writemodel.constants.result_type import ResultType


class ReceiveAcknowledgementCommandHandler(object):
    def __init__(self, event_store: PersistsEventStreams):
        self.__event_store = event_store

    def handle(self, command: ReceiveAcknowledgementCommand) -> ReceiveAcknowledgementResult:
        event_id = command.get_event_id()

        try:
            self.__event_store.acknowledge_event(command.get_consumer_id(), command.get_stream_name(), event_id)

            result = ReceiveAcknowledgementResult()
            result.set_event_id(event_id)

            return result
        except Exception as error:
            return ReceiveAcknowledgementResult(ResultType.FAILURE, str(error))
