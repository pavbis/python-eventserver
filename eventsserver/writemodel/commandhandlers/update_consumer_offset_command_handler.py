from eventsserver.storage.write_event_stores import PersistsEventStreams
from eventsserver.writemodel.commands.update_consumer_offset_command import UpdateConsumerOffsetCommand
from eventsserver.writemodel.results.update_consumer_offset_result import UpdateConsumerOffsetResult
from eventsserver.writemodel.constants.result_type import ResultType


class UpdateConsumerOffsetCommandHandler(object):
    def __init__(self, event_store: PersistsEventStreams):
        self.__event_store = event_store

    def handle(self, command: UpdateConsumerOffsetCommand) -> UpdateConsumerOffsetResult:
        try:
            stream_name = command.get_stream_name()
            consumer_id = command.get_consumer_id()
            event_name = command.get_event_name()
            offset = command.get_offset()

            self.__event_store.update_consumer_offset(stream_name=stream_name, consumer_id=consumer_id,
                                                      event_name=event_name, offset=offset)

            result = UpdateConsumerOffsetResult()
            result.set_event_name(event_name)
            result.set_offset(offset)
            result.set_consumer_id(consumer_id)

            return result
        except Exception as error:
            return UpdateConsumerOffsetResult(ResultType.FAILURE, str(error))
