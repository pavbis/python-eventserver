from pg8000 import Connection
import json
from eventsserver.value.objects import (
    ConsumerId, StreamName, EventName, MaxEventCount, Period, EventId, EventJson, Offset, Event
)
from typing import Iterator
from eventsserver.dto.stream_data import StreamData
from eventsserver.dto.consumer_data import ConsumerData
from eventsserver.dto.event_data import EventData
from eventsserver.storage.expressions.select_streams_expressions import ProvidesPredicate
from eventsserver.storage.exceptions import EventStoreError
from eventsserver.search.specifications.period_specifications import SpecifiesPeriod


class QueriesEvents:
    def get_consumer_id(self) -> ConsumerId:
        raise NotImplementedError

    def get_stream_name(self) -> StreamName:
        raise NotImplementedError

    def get_event_name(self) -> EventName:
        raise NotImplementedError

    def get_max_event_count(self) -> MaxEventCount:
        raise NotImplementedError


class ProvidesEventStreams:
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
                yield Event.from_event_data(event_data=row[1])

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

            return Offset(0 if row is None else int(row[0]))

    def select_streams(self, expression: ProvidesPredicate) -> Iterator[StreamData]:
        with self.__connection.cursor() as cursor:
            query = 'SELECT pSR.*,COALESCE(e.eventscount,0) AS "eventsCount", COALESCE(cOF."consumerCount",' \
                    '0) AS "consumerCount", "firstEventOccurredAt", "lastEventOccurredAt" FROM ' \
                    '"producerStreamRelations" pSR LEFT JOIN (SELECT COUNT(1) AS eventscount, "streamName" AS ' \
                    '"streamName", MIN(e."createdAt") as "firstEventOccurredAt", MAX(e."createdAt") as ' \
                    '"lastEventOccurredAt" FROM events e GROUP BY e."streamName") AS e USING ("streamName") LEFT JOIN ' \
                    '(SELECT COUNT(DISTINCT("consumerId")) AS "consumerCount", "streamName" FROM "consumerOffsets"  ' \
                    'GROUP BY "consumerOffsets"."streamName") AS cOF USING ("streamName") %s ORDER BY pSR."streamName" ' \
                    'DESC' % expression.predicate()

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                yield StreamData.from_list(row)

    def select_consumers_for_stream(self, stream_name: StreamName) -> Iterator[ConsumerData]:
        with self.__connection.cursor() as cursor:
            query = '''
            SELECT
               cOF."consumerId",
               cOF."offset",
               cOF."movedAt",
               e."eventName",
               ROUND(("offset" * 100.0) / COUNT(e."eventId"), 2) AS "consumedPercentage",
               COUNT(e."eventId") - "offset" AS "behind"
            FROM "consumerOffsets" cOF
            INNER JOIN events e USING ("eventName", "streamName")
            WHERE cOF."streamName" = %s
            GROUP BY  e."eventName", cOF."offset", cOF."consumerId", cOF."movedAt"
            '''

            cursor.execute(query, [str(stream_name)])

            rows = cursor.fetchall()

            for row in rows:
                yield ConsumerData.from_list(row)

    def select_events_for_stream(self, stream_name: StreamName, period: SpecifiesPeriod,
                                 expression: ProvidesPredicate) -> Iterator[EventData]:
        pass

    def read_payload_for_event_id(self, event_id: EventId) -> EventJson:
        with self.__connection.cursor() as cursor:
            query = '''
            SELECT e.event::jsonb as "payLoad"
                    FROM events e
                    WHERE e."eventId" = %s
                    LIMIT 1
            '''

            cursor.execute(query, [str(event_id)])
            row = cursor.fetchone()

            if row is None:
                raise EventStoreError('Event with id %s not found.' % str(event_id))

            return EventJson(json.dumps(row[0]))

