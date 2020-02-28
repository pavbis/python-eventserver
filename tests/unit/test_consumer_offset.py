from uuid import uuid4
from unittest import TestCase
from eventsserver.metrics.metrics_types import ConsumerOffset


class ConsumerOffsetTest(TestCase):
    def test_it_can_be_created_from_list(self):
        primitive_consumer_id = str(uuid4())
        primitive_list = [primitive_consumer_id, 'test', 10, 'boo']

        consumer_offset = ConsumerOffset.from_list(primitive_list)

        self.assertEqual('test', str(consumer_offset.get_stream_name()))
        self.assertEqual(10, int(consumer_offset.get_offset()))
        self.assertEqual(primitive_consumer_id, str(consumer_offset.get_consumer_id()))
        self.assertEqual('boo', str(consumer_offset.get_event_name()))
