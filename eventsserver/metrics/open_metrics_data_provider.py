from eventsserver.metrics.metrics_storage import ProvidesMetrics
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, CollectorRegistry
from prometheus_client import generate_latest


class EventServerCollector(object):
    __METRIC_STREAMS_TOTAL = 'streams'
    __METRIC_EVENTS_TOTAL = 'events'
    __METRIC_CONSUMERS_TOTAL = 'consumers'
    __METRIC_PRODUCERS_TOTAL = 'producers'
    __METRIC_CONSUMER_OFFSET = 'consumer_offset'

    def __init__(self, storage: ProvidesMetrics):
        self.__storage = storage

    def collect(self):
        """
        Streams total metric
        """
        yield CounterMetricFamily(
            self.__METRIC_STREAMS_TOTAL,
            'Total amount of streams created on the server',
            int(self.__storage.streams_total())
        )

        """
        Events in stream metric
        """
        events_in_stream_metric = CounterMetricFamily(self.__METRIC_EVENTS_TOTAL, 'Total amount of events per stream')

        for events_in_stream in self.__storage.events_in_streams_with_owner():
            events_in_stream_metric.add_sample(
                events_in_stream_metric.name + '_total',
                {
                    "streamName": str(events_in_stream.get_stream_name()),
                    'producerId': str(events_in_stream.get_producer_id())
                },
                int(events_in_stream.get_events())
            )

        yield events_in_stream_metric

        """
        Consumers total metric
        """

        consumers_total_metric = CounterMetricFamily(
            self.__METRIC_CONSUMERS_TOTAL, 'Total amount of registered consumers per stream'
        )

        for consumer_total in self.__storage.consumers_in_stream():
            consumers_total_metric.add_sample(
                consumers_total_metric.name + '_total',
                {'streamName': str(consumer_total.get_stream_name())},
                int(consumer_total.get_consumers_count())
            )

        yield consumers_total_metric

        """
        Producers total metric
        """

        yield CounterMetricFamily(
            self.__METRIC_PRODUCERS_TOTAL,
            'Total amount of registered producers on the server',
            int(self.__storage.streams_total())
        )

        """
        Consumer offset per event metric
        """

        consumers_offset_metric = GaugeMetricFamily(
            self.__METRIC_CONSUMER_OFFSET,
            'Current offset of consumers per stream and event'
        )

        for consumer_offset in self.__storage.consumer_offsets():
            consumers_offset_metric.add_sample(
                consumers_offset_metric.name + '_total',
                {
                    'streamName': str(consumer_offset.get_stream_name()),
                    'eventName': str(consumer_offset.get_event_name()),
                    'consumerId': str(consumer_offset.get_consumer_id()),
                },
                int(consumer_offset.get_offset())
            )

        yield consumers_offset_metric


class OpenMetricsDataProvider:

    def __init__(self, storage: ProvidesMetrics):
        self.__storage = storage

    def read_metrics(self):
        registry = CollectorRegistry(auto_describe=False)
        registry.register(EventServerCollector(self.__storage))

        return generate_latest(registry)
