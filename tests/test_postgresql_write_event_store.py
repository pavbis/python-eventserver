from unittest import TestCase
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.value.objects import (
    ProducerId,
    StreamName,
    EventJson,
    EventId
)
from eventsserver.storage.write_event_stores import PostgreSqlWriteEventStore, StreamReservedForProducer
import uuid
import json


class PostgreSQLWriteEventStoreTest(TestCase):
    def setUp(self) -> None:
        self.database_manager = DataBaseManager()
        self.database_manager.create_schema()
        self.connection = self.database_manager.connection()
        self.event_store = PostgreSqlWriteEventStore(self.connection)

    def test_it_raises_stream_reserved_for(self):
        http_payload = {'event': {'name': 'Snickers', 'version': 1},
                        'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                                   'timezone': 'Europe/Berlin'},
                        'payload': {'foo': 'bar'}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

        stream_name = StreamName('Unit-Test')
        producer_id_one = ProducerId(str(uuid.uuid4()))
        producer_id_two = ProducerId(str(uuid.uuid4()))
        event_id = EventId(str(uuid.uuid4()))
        event = EventJson(json.dumps(http_payload)).to_event_with_id(event_id)

        self.event_store.record_event(producer_id_one, stream_name, event)

        with self.assertRaises(StreamReservedForProducer) as context:
            self.event_store.record_event(producer_id_two, stream_name, event)
        self.assertTrue(
            'Stream is reserved for another producer: {}'.format(str(producer_id_one)) in str(context.exception)
        )

    def tearDown(self) -> None:
        self.database_manager.truncate_tables()
