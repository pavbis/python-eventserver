import uuid
from unittest import TestCase
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.value.objects import (
    StreamName,
    EventId,
    ConsumerId
)
from eventsserver.storage.write_event_stores import PostgreSqlWriteEventStore
from eventsserver.storage.exceptions import EventStoreError


class PostgreSQLWriteEventStoreTest(TestCase):

    def setUp(self) -> None:
        self.STREAM_NAME = 'nicowa'
        self.database_manager = DataBaseManager()
        self.event_store = PostgreSqlWriteEventStore(self.database_manager.connection())
        self.payload = {'event': {'name': 'Snickers', 'version': 1},
                        'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                                   'timezone': 'Europe/Berlin'},
                        'payload': {'foo': 'bar'}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

    def test_acknowledge_event_raises_event_not_found_in_stream(self):
        stream_name = StreamName(self.STREAM_NAME)
        consumer_id = ConsumerId(str(uuid.uuid4()))
        not_existent_event_id = EventId(str(uuid.uuid4()))

        with self.assertRaises(EventStoreError) as context:
            self.event_store.acknowledge_event(consumer_id, stream_name, not_existent_event_id)
        self.assertTrue(
            'Event not found in stream: {}/{}'.format(str(stream_name), str(not_existent_event_id)) in str(
                context.exception)
        )
