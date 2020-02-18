from typing import Optional
from eventsserver.value.objects import (
    StreamName,
    ProducerId,
    Event,
    ConsumerId,
    EventId,
    EventName,
    Offset,
    EventCount
)
from pg8000 import Connection
from eventsserver.storage.exceptions import StreamReservedForProducer, EventStoreError


class PersistsEventStreams(object):
    def record_event(self, producer_id: ProducerId, stream_name: StreamName, event: Event) -> None:
        raise NotImplementedError

    def acknowledge_event(self, consumer_id: ConsumerId, stream_name: StreamName, event_id: EventId) -> None:
        raise NotImplementedError

    def update_consumer_offset(
            self, stream_name: StreamName, consumer_id: ConsumerId, event_name: EventName, offset: Offset
    ) -> None:
        raise NotImplementedError


class PostgreSqlWriteEventStore(PersistsEventStreams):
    def __init__(self, connection: Connection):
        self.connection = connection

    def close(self):
        self.connection.close()

    def record_event(self, producer_id: ProducerId, stream_name: StreamName, event: Event) -> None:
        try:
            related_producer_id = self.__fetch_producer_id_for_stream_name(stream_name)

            if related_producer_id is None:
                self.__save_producer_stream_relation(producer_id, stream_name)
                related_producer_id = producer_id

            if related_producer_id != producer_id:
                raise StreamReservedForProducer(
                    'Stream is reserved for another producer: {}'.format(str(related_producer_id))
                )

            with self.connection.cursor() as cursor:
                query = 'INSERT INTO "events" ("streamName", "eventName", "sequence", "eventId", "event") VALUES (%s, ' \
                        '%s, ' \
                        '(SELECT COALESCE(MAX("sequence"),0) FROM "events" WHERE "streamName" = %s AND "eventName" = ' \
                        '%s ' \
                        'LIMIT 1) + 1, %s, %s)'

                cursor.execute(
                    query,
                    [
                        str(stream_name), str(event.event_name), str(stream_name),
                        str(event.event_name), str(event.event_id), event.to_json()
                    ]
                )
                self.connection.commit()
                self.connection.close()
        except self.connection.DatabaseError as error:
            self.connection.rollback()
            print(error)
        finally:
            if self.connection.in_transaction:
                self.connection.close()

    def __save_producer_stream_relation(self, producer_id: ProducerId, stream_name: StreamName) -> None:
        query = 'INSERT INTO "producerStreamRelations" ("producerId", "streamName") VALUES (%s, %s) ON CONFLICT (' \
                '"streamName") DO NOTHING'

        cursor = self.connection.cursor()
        cursor.execute(query, [str(producer_id), str(stream_name)])

    def __fetch_producer_id_for_stream_name(self, stream_name: StreamName) -> Optional[ProducerId]:
        with self.connection.cursor() as cursor:
            query = 'SELECT "producerId" FROM "producerStreamRelations" WHERE "streamName" = %s LIMIT 1'
            cursor.execute(query, [str(stream_name)])

            producer_id = cursor.fetchone()

            if producer_id is None:
                return producer_id
            else:
                return ProducerId(producer_id[0])

    def acknowledge_event(self, consumer_id: ConsumerId, stream_name: StreamName, event_id: EventId) -> None:
        event_name, sequence = self.__get_event_name_and_sequence(stream_name, event_id)
        consumer_offset = self.__get_consumer_offset(consumer_id, stream_name, event_name)
        next_offset = consumer_offset.increment()

        if next_offset != sequence:
            raise EventStoreError('Consumer offset mismatch: {}->{}'.format(str(next_offset), str(sequence)))

        query = 'INSERT INTO "consumerOffsets" ("consumerId", "streamName", "eventName", "offset") VALUES (%s, %s, ' \
                '%s, %s) ON CONFLICT ("consumerId", "streamName", "eventName") DO UPDATE SET "offset" = ' \
                'EXCLUDED."offset", "movedAt" = now()'

        cursor = self.connection.cursor()
        cursor.execute(query, [str(consumer_id), str(stream_name), str(event_name), int(next_offset)])

    def __get_consumer_offset(self, consumer_id: ConsumerId, stream_name: StreamName, event_name: EventName) -> Offset:
        with self.connection.cursor() as cursor:
            query = 'SELECT "offset" FROM "consumerOffsets" WHERE "consumerId" = %s AND "eventName" = %s AND ' \
                    '"streamName" = %s LIMIT 1 '
            cursor.execute(query, [str(consumer_id), str(event_name), str(stream_name)])

            row = cursor.fetchone()

            return Offset(0 if row is None else int(row[0]))

    def __get_event_name_and_sequence(self, stream_name: StreamName, event_id: EventId):
        with self.connection.cursor() as cursor:
            query = 'SELECT "eventName", "sequence" FROM "events" WHERE "streamName" = %s AND "eventId" = %s LIMIT 1'
            cursor.execute(query, [str(stream_name), str(event_id)])

            row = cursor.fetchone()

            if row is None:
                raise EventStoreError('Event not found in stream: {}/{}'.format(str(stream_name), str(event_id)))

            event_name = EventName(row[0])
            sequence = Offset(row[1])

            return [event_name, sequence]

    def update_consumer_offset(
            self, stream_name: StreamName, consumer_id: ConsumerId, event_name: EventName, offset: Offset
    ) -> None:
        event_count = self.__count_events_for_consumer(stream_name, consumer_id, event_name)

        if int(offset) > int(event_count):
            raise EventStoreError(
                'Offset {} can not be greater than event count {}.'.format(int(offset), int(event_count))
            )

        query = 'UPDATE "consumerOffsets" SET "offset" = %s, "movedAt" = now() WHERE "consumerId" = %s AND ' \
                '"eventName" = %s AND "streamName" = %s '

        cursor = self.connection.cursor()
        cursor.execute(query, [int(offset), str(consumer_id), str(event_name), str(stream_name)])

    def __count_events_for_consumer(
            self, stream_name: StreamName, consumer_id: ConsumerId, event_name: EventName) -> EventCount:
        with self.connection.cursor() as cursor:
            query = 'SELECT COALESCE(COUNT(e."eventId"), 0) FROM events e LEFT JOIN "consumerOffsets" cO USING (' \
                    '"eventName", "streamName") WHERE e."streamName" = %s AND e."eventName" = %s AND ' \
                    'cO."consumerId" = %s'

            cursor.execute(query, [str(stream_name), str(event_name), str(consumer_id)])

            row = cursor.fetchone()

            return EventCount(row[0])
