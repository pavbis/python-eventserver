from eventsserver.value.objects import (
    ConsumerId, StreamName, EventName, MaxEventCount, Period, EventId, EventJson, Offset, Event
)
from typing import Iterator
from eventsserver.dto.stream_data import StreamData
from eventsserver.dto.consumer_data import ConsumerData
from eventsserver.dto.event_data import EventData
from pg8000 import Connection


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


class SpecifiesPeriod(object):
    def is_satisfied_by(self, period: Period) -> bool:
        raise NotImplementedError

    def and_expression(self) -> str:
        raise NotImplementedError

    def period(self) -> str:
        raise NotImplementedError

    def period_literal(self) -> str:
        raise NotImplementedError


class ProvidesPredicate(object):
    def predicate(self) -> str:
        raise NotImplementedError

    def search_criteria(self) -> ContainsSearchCriteria:
        raise NotImplementedError


class ProvidesEventStreams(object):
    def select_events(self, query: QueriesEvents) -> Iterator[Event]:
        raise NotImplementedError

    def select_streams(self, expression: ProvidesPredicate) -> Iterator[StreamData]:
        raise NotImplementedError

    def select_consumers_for_stream(self, stream_name: StreamName) -> Iterator[ConsumerData]:
        raise NotImplementedError

    def select_events_for_stream(
            self, stream_name: StreamName, period: SpecifiesPeriod, expression: ProvidesPredicate
    ) -> Iterator[EventData]:
        raise NotImplementedError

    def read_payload_for_event_id(self, event_id: EventId) -> EventJson:
        raise NotImplementedError


class PostgreSqlReadEventStore(ProvidesEventStreams):

    def __init__(self, connection: Connection):
        self.__connection = connection

    def select_events(self, query: QueriesEvents) -> Iterator[Event]:
        consumer_offset = self.__get_consumer_offset(
            consumer_id=query.get_consumer_id(), stream_name=query.get_stream_name(), event_name=query.get_event_name()
        )

        with self.__connection.cursor() as cursor:
            sql_query = '''
            SELECT "sequence", "event" 
                FROM "events" 
                WHERE "streamName" = %s 
                AND "eventName" = %s 
                AND "sequence" > %s
                ORDER BY "sequence" ASC 
                LIMIT %s
            '''

            cursor.execute(
                sql_query,
                [
                    str(query.get_stream_name()), str(query.get_event_name()),
                    int(consumer_offset), int(query.get_max_event_count())
                ]
            )

            rows = cursor.fetchall()

            for row in rows:
                yield Event.from_event_data(event_data=row)

    def __get_consumer_offset(self, consumer_id: ConsumerId, stream_name: StreamName, event_name: EventName) -> Offset:
        with self.__connection.cursor() as cursor:
            query = '''
            SELECT "offset" FROM "consumerOffsets" 
                    WHERE "consumerId" = %s
                    AND "streamName" = %s
                    AND "eventName" = %s
                    LIMIT 1
            '''

            cursor.execute(query, [str(consumer_id), str(stream_name), str(event_name)])
            row = cursor.fetchone()

            return Offset(0)

    def select_streams(self, expression: ProvidesPredicate) -> Iterator[StreamData]:
        pass

    def select_consumers_for_stream(self, stream_name: StreamName) -> Iterator[ConsumerData]:
        pass

    def select_events_for_stream(self, stream_name: StreamName, period: SpecifiesPeriod,
                                 expression: ProvidesPredicate) -> Iterator[EventData]:
        pass

    def read_payload_for_event_id(self, event_id: EventId) -> EventJson:
        pass
