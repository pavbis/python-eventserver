from uuid import uuid4
from unittest import TestCase
from eventsserver.metrics.metrics_types import StreamTotals


class StreamTotalsTest(TestCase):
    def test_it_can_be_created_from_list(self):
        primitive_producer_id = str(uuid4())
        primitive_list = ['test', primitive_producer_id, 10]

        stream_totals = StreamTotals.from_list(primitive_list)

        self.assertEqual('test', str(stream_totals.get_stream_name()))
        self.assertEqual(primitive_producer_id, str(stream_totals.get_producer_id()))
        self.assertEqual(10, int(stream_totals.get_events()))
