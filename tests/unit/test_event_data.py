from unittest import TestCase
from eventsserver.dto.event_data import EventData
import uuid


class EventDataTest(TestCase):

    def test_event_data_can_be_created_without_producer_ids(self) -> None:
        event_id = str(uuid.uuid4())

        primitive_list = ['unit-test', '2019-11-09 08:38:35.806000+00:00', None, event_id]

        event_data = EventData.from_list(primitive_list)

        self.assertEqual('unit-test', str(event_data.get_event_name()))
        self.assertEqual('2019-11-09 08:38:35.806000+00:00', str(event_data.get_created_at()))
        self.assertEqual(event_id, str(event_data.get_event_id()))
        self.assertEqual(0, len(event_data.get_consumer_ids()))

    def test_event_data_can_be_created_with_producer_ids(self) -> None:

        uuid_1 = str(uuid.uuid4())
        uuid_2 = str(uuid.uuid4())
        event_id = str(uuid.uuid4())
        uuids = '%s, %s' % (uuid_1, uuid_2)

        primitive_list = ['unit-test', '2019-11-08 08:38:35.806000+00:00', uuids, event_id]

        event_data = EventData.from_list(primitive_list)

        self.assertEqual('unit-test', str(event_data.get_event_name()))
        self.assertEqual('2019-11-08 08:38:35.806000+00:00', str(event_data.get_created_at()))
        self.assertEqual(event_id, str(event_data.get_event_id()))
        self.assertEqual(2, len(event_data.get_consumer_ids()))
        self.assertEqual(uuid_1, str(event_data.get_consumer_ids()[0]))
        self.assertEqual(uuid_2, str(event_data.get_consumer_ids()[-1]))
