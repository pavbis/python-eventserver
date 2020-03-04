from typing import Iterator
from unittest import TestCase
import itertools
from pathlib import Path

from eventsserver.metrics.metrics_types import ConsumerOffset, ConsumerTotals, StreamTotals, StreamCount
from eventsserver.metrics.open_metrics_data_provider import OpenMetricsDataProvider
from eventsserver.metrics.metrics_storage import ProvidesMetrics


class FakeMetricsStorage(ProvidesMetrics):

    def streams_total(self) -> StreamCount:
        return StreamCount(10)

    def events_in_streams_with_owner(self) -> Iterator[StreamTotals]:
        producer_id = '7b13bcba-a18f-4887-b784-9417262862e4'
        stream_totals_fixture = [['foo', producer_id, 10], ['bar', producer_id, 20]]
        iterator = iter([])

        for stream_totals in stream_totals_fixture:
            iterator = itertools.chain([StreamTotals.from_list(stream_totals)], iterator)

        return iterator

    def consumers_in_stream(self) -> Iterator[ConsumerTotals]:
        consumer_totals_fixture = [['foo', 10], ['bar', 20]]
        iterator = iter([])

        for consumer_totals in consumer_totals_fixture:
            iterator = itertools.chain([ConsumerTotals.from_list(consumer_totals)], iterator)

        return iterator

    def consumer_offsets(self) -> Iterator[ConsumerOffset]:
        consumer_offset_fixture = [
            ['72b53044-3194-4378-b71b-b62c1986be92', 'foo', 10, 'event_1'],
            ['72b53044-3194-4378-b71b-b62c1986be92', 'bar', 20, 'event_2']
        ]
        iterator = iter([])

        for consumer_offset in consumer_offset_fixture:
            iterator = itertools.chain([ConsumerOffset.from_list(consumer_offset)], iterator)

        return iterator


class OpenMetricsDataProviderTest(TestCase):
    def test_it_returns_formatted_metrics(self) -> None:
        data_provider = OpenMetricsDataProvider(FakeMetricsStorage())

        self.assertEqual(Path('tests/unit/metrics.txt').read_text(), str(data_provider.read_metrics()))
