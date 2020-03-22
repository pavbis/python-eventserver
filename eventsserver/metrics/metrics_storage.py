from typing import Iterator
from pg8000 import Connection
from eventsserver.metrics.metrics_types import StreamCount, StreamTotals, ConsumerTotals, ConsumerOffset


class ProvidesMetrics:
    def streams_total(self) -> StreamCount:
        raise NotImplementedError

    def events_in_streams_with_owner(self) -> Iterator[StreamTotals]:
        raise NotImplementedError

    def consumers_in_stream(self) -> Iterator[ConsumerTotals]:
        raise NotImplementedError

    def consumer_offsets(self) -> Iterator[ConsumerOffset]:
        raise NotImplementedError


class PostgreSqlMetricsStorage(ProvidesMetrics):
    def __init__(self, connection: Connection):
        self.__connection = connection

    def streams_total(self) -> StreamCount:
        with self.__connection.cursor() as cursor:
            cursor.execute(
                '''SELECT COALESCE(COUNT(pSR."producerId"), 0) as "streamCount"
                    FROM "producerStreamRelations" pSR'''
            )

            row = cursor.fetchone()

            return StreamCount(row[0])

    def events_in_streams_with_owner(self) -> Iterator[StreamTotals]:
        with self.__connection.cursor() as cursor:
            cursor.execute('''SELECT
                    pSR."streamName",
                    pSR."producerId",
                    COALESCE(COUNT(e."eventId"), 0) as "eventCount"
                FROM "producerStreamRelations" pSR
                    LEFT JOIN events e USING ("streamName")
                GROUP BY pSR."streamName", pSR."producerId"''')

            rows = cursor.fetchall()

            for row in rows:
                yield StreamTotals.from_list(row)

    def consumers_in_stream(self) -> Iterator[ConsumerTotals]:
        with self.__connection.cursor() as cursor:
            cursor.execute('''SELECT
                    cOF."streamName",
                    COALESCE(COUNT(DISTINCT cOF."consumerId"), 0) as "countConsumer"
                FROM "consumerOffsets" cOF
                GROUP BY cOF."streamName"''')

            rows = cursor.fetchall()

            for row in rows:
                yield ConsumerTotals.from_list(row)

    def consumer_offsets(self) -> Iterator[ConsumerOffset]:
        with self.__connection.cursor() as cursor:
            cursor.execute('''SELECT
                cOF."consumerId",
                cOF."streamName",
                cOF."offset",
                cOF."eventName"
            FROM "consumerOffsets" cOF 
            ORDER BY "streamName";''')

            rows = cursor.fetchall()

            for row in rows:
                yield ConsumerOffset.from_list(row)
