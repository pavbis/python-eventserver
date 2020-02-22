from unittest import TestCase
from eventsserver.storage.read_event_stores import PostgreSqlReadEventStore
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.value.objects import EventId
from eventsserver.storage.exceptions import EventStoreError


class PostgreSqlReadEventStoreTest(TestCase):
    def setUp(self) -> None:
        self.database_manager = DataBaseManager()
        self.event_store = PostgreSqlReadEventStore(self.database_manager.connection())

    def test_read_event_payload_returns_payload(self) -> None:
        payload = self.event_store.read_payload_for_event_id(EventId('ebf1e616-ca51-4f76-908d-d5781c0ad550'))

        self.assertEqual('{"event": {"id": "ebf1e616-ca51-4f76-908d-d5781c0ad550", "name": "Snickers", "version": 1}, '
                         '"system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", '
                         '"timezone": '
                         '"Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", "type": '
                         '"system"}}',
                         str(payload))

    def test_read_event_payload_throws_exception_if_event_not_exists(self) -> None:
        plain_event_id = '2480b859-e08a-4414-9c7d-003bc1a4b221'

        with self.assertRaises(EventStoreError) as context:
            self.event_store.read_payload_for_event_id(EventId(plain_event_id))
        self.assertTrue(
            'Event with id %s not found.' % str(plain_event_id) in str(context.exception)
        )
