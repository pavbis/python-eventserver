from unittest import TestCase
from tests.unit.fakes.storage.in_memory_write_event_store import InMemoryWriteEventStore
from eventsserver.writemodel.commandhandlers.receive_acknowledgement_command_handler import \
    ReceiveAcknowledgementCommandHandler
from eventsserver.writemodel.commands.receive_acknowledgement_command import ReceiveAcknowledgementCommand
from eventsserver.value.objects import ConsumerId, StreamName, EventId
import uuid


class ReceiveAcknowledgementCommandHandlerTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryWriteEventStore()
        self.event_store.reset()
        self.command_handler = ReceiveAcknowledgementCommandHandler(self.event_store)

    def test_it_returns_success_result(self) -> None:
        consumer_id = ConsumerId(str(uuid.uuid4()))
        stream_name = StreamName('test')
        event_id = EventId(str(uuid.uuid4()))

        command = ReceiveAcknowledgementCommand(consumer_id, stream_name, event_id)

        result = self.command_handler.handle(command)

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(str(event_id), str(result.get_event_id()))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.event_store.will_raise_database_error()

        consumer_id = ConsumerId(str(uuid.uuid4()))
        stream_name = StreamName('test')
        event_id = EventId(str(uuid.uuid4()))

        command = ReceiveAcknowledgementCommand(consumer_id, stream_name, event_id)

        result = self.command_handler.handle(command)

        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_ACKNOWLEDGE_EVENT_ERROR, str(result.get_message()))
