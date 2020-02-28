from unittest import TestCase
from eventsserver.metrics.metrics_types import ConsumerTotals


class ConsumerTotalsTest(TestCase):
    def test_it_can_be_created_from_list(self):
        primitive_list = ['test', 10]

        consumer_totals = ConsumerTotals.from_list(primitive_list)

        self.assertEqual('test', str(consumer_totals.get_stream_name()))
        self.assertEqual(10, int(consumer_totals.get_consumers_count()))
