from unittest import TestCase
from eventsserver.writemodel.commandhandlers.receive_event_command_handler import ReceiveEventCommandHandler
from eventsserver.writemodel.commands.receive_event_command import ReceiveEventCommand
from eventsserver.value.objects import EventId, ProducerId, StreamName, EventJson
from tests.unit.fakes.storage.in_memory_write_event_store import InMemoryWriteEventStore
from eventsserver.writemodel.results.receive_event_result import ReceiveEventResult
import uuid
import json


class ReceiveEventCommandHandlerTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryWriteEventStore()
        self.event_store.reset()
        self.command_handler = ReceiveEventCommandHandler(self.event_store)

    def test_it_returns_success_result(self) -> None:
        producer_id = ProducerId(str(uuid.uuid4()))
        event_id = EventId(str(uuid.uuid4()))
        result = self.__handle_command(event_id, producer_id)

        self.assertEqual(1, len(self.event_store.events))
        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(str(event_id), str(result.get_event_id()))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.event_store.will_raise_database_error()
        event_id = EventId(str(uuid.uuid4()))
        producer_id = ProducerId(str(uuid.uuid4()))
        result = self.__handle_command(event_id, producer_id)

        self.assertEqual(0, len(self.event_store.events))
        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_RECORD_EVENT_ERROR, result.get_message())

    def __handle_command(self, event_id: EventId, producer_id: ProducerId) -> ReceiveEventResult:
        stream_name = StreamName('test')

        event_data = {'event': {'name': 'Snickers', 'version': 1},
                      'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                                 'timezone': 'Europe/Berlin'},
                      'payload': {'foo': 'bar'}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

        event_json = EventJson(json.dumps(event_data))
        command = ReceiveEventCommand(event_id, producer_id, stream_name, event_json)
        return self.command_handler.handle(command)
