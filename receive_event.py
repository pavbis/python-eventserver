from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.storage.write_event_stores import PostgreSqlWriteEventStore
from eventsserver.writemodel.commandhandlers.receive_event_command_handler import ReceiveEventCommandHandler
from eventsserver.writemodel.commands.receive_event_command import ReceiveEventCommand
from eventsserver.value.objects import ProducerId, EventId, StreamName, EventJson
import uuid
import json


def receive_event():
    database_manager = DataBaseManager()
    connection = database_manager.connection()
    event_store = PostgreSqlWriteEventStore(connection=connection)
    receive_event_command_handler = ReceiveEventCommandHandler(event_store=event_store)

    producer_id = ProducerId(str(uuid.uuid4()))
    event_id = EventId('c3f390b8-302f-49af-b987-66ab0a931a62')
    stream_name = StreamName('python')

    event_data = {'event': {'name': 'Snickers', 'version': 1},
                  'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                             'timezone': 'Europe/Berlin'},
                  'payload': {'foo': 'bar'}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

    event_json = EventJson(json.dumps(event_data))
    receive_event_command = ReceiveEventCommand(
        event_id=event_id, producer_id=producer_id, stream_name=stream_name, event_json=event_json
    )
    result = receive_event_command_handler.handle(command=receive_event_command)

    print(result.succeeded())
    print(str(result.get_event_id()))
    print(result.get_message())


if __name__ == '__main__':
    receive_event()
