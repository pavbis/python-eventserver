from unittest import TestCase
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.value.objects import (
    ProducerId,
    StreamName,
    EventJson,
    EventId,
    ConsumerId
)
from eventsserver.storage.write_event_stores import PostgreSqlWriteEventStore
from eventsserver.storage.exceptions import EventStoreError, StreamReservedForProducer
import uuid
import json
import pg8000
from eventsserver.config.parser import config


def connection():
    connection_parameters = config('eventsserver/config/database.ini', 'postgresql')

    return pg8000.connect(**connection_parameters)


class PostgreSQLWriteEventStoreTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.STREAM_NAME = 'Unit-Test'
        cls.database_manager = DataBaseManager()
        cls.database_manager.create_schema()
        cls.connection = cls.database_manager.connection()
        cls.event_store = PostgreSqlWriteEventStore(connection())
        cls.event_store_another_instance = PostgreSqlWriteEventStore(connection())
        cls.payload = {'event': {'name': 'Snickers', 'version': 1},
                       'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                                  'timezone': 'Europe/Berlin'},
                       'payload': {'foo': 'bar'}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

    def test_record_event_raises_stream_reserved_for(self):
        stream_name = StreamName(self.STREAM_NAME)
        producer_id_one = ProducerId(str(uuid.uuid4()))
        producer_id_two = ProducerId(str(uuid.uuid4()))
        event_id = EventId(str(uuid.uuid4()))
        event = EventJson(json.dumps(self.payload)).to_event_with_id(event_id)

        self.event_store.record_event(producer_id_one, stream_name, event)

        with connection().cursor() as cursor:
            cursor.execute('SELECT * FROM "producerStreamRelations"')

            row = cursor.fetchone()

            connection().close()

            self.assertEqual(str(producer_id_one), row[0])
            self.assertEqual(self.STREAM_NAME, row[1])

        with self.assertRaises(StreamReservedForProducer) as context:
            self.event_store_another_instance.record_event(producer_id_two, stream_name, event)
        self.assertTrue(
            'Stream is reserved for another producer: {}'.format(str(producer_id_one)) in str(context.exception)
        )

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

    @classmethod
    def tearDownClass(cls):
        cls.database_manager = DataBaseManager()
        cls.database_manager.truncate_tables()
