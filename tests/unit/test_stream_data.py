from unittest import TestCase
from eventsserver.dto.stream_data import StreamData


class StreamDataTest(TestCase):
    def test_stream_data_can_be_created_from_list(self) -> None:
        primitive_list = [
            'c3f390b8-302f-49af-b987-66ab0a931a62', 'unit-test', 1,
            2, '2019-11-08 08:38:35.806000+00:00', '2019-11-26 09:02:29.418000+00:00'
        ]

        stream_data = StreamData.from_list(primitive_list)

        self.assertEqual('c3f390b8-302f-49af-b987-66ab0a931a62', str(stream_data.get_producer_id()))
        self.assertEqual('unit-test', str(stream_data.get_stream_name()))
        self.assertEqual(1, int(stream_data.get_events_count()))
        self.assertEqual(2, int(stream_data.get_consumer_count()))
        self.assertEqual('2019-11-08 08:38:35.806000+00:00', str(stream_data.get_first_event_occurred_at()))
        self.assertEqual('2019-11-26 09:02:29.418000+00:00', str(stream_data.get_last_event_occurred_at()))
