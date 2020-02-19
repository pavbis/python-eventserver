from unittest import TestCase
from tests.unit.fakes.storage.in_memory_write_event_store import InMemoryWriteEventStore
from eventsserver.writemodel.commandhandlers.update_consumer_offset_command_handler import \
    UpdateConsumerOffsetCommandHandler
from eventsserver.writemodel.commands.update_consumer_offset_command import UpdateConsumerOffsetCommand
from eventsserver.value.objects import ConsumerId, StreamName, EventName, Offset
import uuid


class UpdateConsumerOffsetCommandHandlerTest(TestCase):
    def setUp(self) -> None:
        self.event_store = InMemoryWriteEventStore()
        self.event_store.reset()
        self.command_handler = UpdateConsumerOffsetCommandHandler(self.event_store)

    def test_it_returns_success_result(self) -> None:
        consumer_id = ConsumerId(str(uuid.uuid4()))
        stream_name = StreamName('test')
        event_name = EventName('foo')
        offset = Offset(10)

        command = UpdateConsumerOffsetCommand(consumer_id, stream_name, event_name, offset)

        result = self.command_handler.handle(command)

        self.assertTrue(result.succeeded())
        self.assertEqual('', result.get_message())
        self.assertEqual(str(result.get_offset()), str(offset))
        self.assertEqual(str(result.get_event_name()), str(event_name))
        self.assertEqual(str(result.get_consumer_id()), str(consumer_id))

    def test_it_returns_failure_if_event_store_exception_raised(self):
        self.event_store.will_raise_database_error()

        consumer_id = ConsumerId(str(uuid.uuid4()))
        stream_name = StreamName('test')
        event_name = EventName('foo')
        offset = Offset(10)

        command = UpdateConsumerOffsetCommand(consumer_id, stream_name, event_name, offset)

        result = self.command_handler.handle(command)

        self.assertTrue(result.failure())
        self.assertEqual(self.event_store.EVENT_STORE_UPDATE_CONSUMER_OFFSET_ERROR, result.get_message())

