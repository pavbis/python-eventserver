from eventsserver.value.objects import ConsumerId, StreamName, EventName, MaxEventCount
from typing import Generator
from eventsserver.dto.stream_data import StreamData


class QueriesEvents(object):
    def get_consumer_id(self) -> ConsumerId:
        raise NotImplementedError

    def get_stream_name(self) -> StreamName:
        raise NotImplementedError

    def get_event_name(self) -> EventName:
        raise NotImplementedError

    def get_max_event_count(self) -> MaxEventCount:
        raise NotImplementedError


class ContainsSearchCriteria(object):
    pass


class ProvidesPredicate(object):
    def predicate(self) -> str:
        raise NotImplementedError

    def search_criteria(self) -> ContainsSearchCriteria:
        raise NotImplementedError


class ProvidesEventStreams(object):
    def select_events(self, query: QueriesEvents):
        raise NotImplementedError

    def select_streams(self, expression: ProvidesPredicate) -> Generator[StreamData]:
        raise NotImplementedError

    def select_consumers_for_stream(self, stream_name: StreamName):
        pass
