from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.storage.write_event_stores import PostgreSqlWriteEventStore
from eventsserver.writemodel.commandhandlers.receive_acknowledgement_command_handler import \
    ReceiveAcknowledgementCommandHandler
from eventsserver.writemodel.commands.receive_acknowledgement_command import ReceiveAcknowledgementCommand
from eventsserver.value.objects import ConsumerId, StreamName, EventId
import uuid


def acknowledge_event():
    database_manager = DataBaseManager()
    connection = database_manager.connection()
    event_store = PostgreSqlWriteEventStore(connection=connection)
    stream_name = StreamName('python')
    event_id = EventId('c3f390b8-302f-49af-b987-66ab0a931a62')

    consumer_id = ConsumerId(str(uuid.uuid4()))
    command = ReceiveAcknowledgementCommand(consumer_id=consumer_id, stream_name=stream_name, event_id=event_id)

    command_handler = ReceiveAcknowledgementCommandHandler(event_store=event_store)
    result = command_handler.handle(command=command)

    print(result.succeeded())
    print(result.get_message())
    print(result.get_event_id())


if __name__ == '__main__':
    acknowledge_event()
