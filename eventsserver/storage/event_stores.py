from typing import Optional
import json

from eventsserver.value.event import Event
from eventsserver.value.objects import (
    StreamName,
    ProducerId
)

from pg8000 import Connection
from eventsserver.storage.exceptions import StreamReservedForProducer


class PersistsEventStreams(object):
    def record_event(self, producer_id: ProducerId, stream_name: StreamName, event: Event) -> None:
        raise NotImplementedError

    def acknowledge_event(self) -> None:
        raise NotImplementedError

    def update_consumer_offset(self) -> None:
        raise NotImplementedError


class PostgreSqlWriteEventStore(PersistsEventStreams):
    def __init__(self, connection: Connection):
        self.connection = connection

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

            foo = {"event": {"id": "c3f390b8-302f-49af-b987-66ab0a931a62", "name": "Snickers", "version": 1},
                   "system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12",
                              "timezone": "Europe/Berlin"}, "payload": {},
                   "trigger": {"name": "/path/to/script.php", "type": "system"}}

            query = 'INSERT INTO "events" ("streamName", "eventName", "sequence", "eventId", "event") VALUES (%s, %s, ' \
                    '(SELECT COALESCE(MAX("sequence"),0) FROM "events" WHERE "streamName" = %s AND "eventName" = %s ' \
                    'LIMIT 1) + 1, %s, %s)'

            cursor = self.connection.cursor()
            cursor.execute(
                query,
                [
                    str(stream_name), str(event.event_name), str(stream_name),
                    str(event.event_name), str(event.event_id), json.dumps(foo)
                ]
            )

            self.connection.commit()
        except self.connection.DatabaseError as error:
            self.connection.rollback()
            print(error)
        finally:
            if self.connection.in_transaction:
                self.connection.close()

    def acknowledge_event(self) -> None:
        pass

    def update_consumer_offset(self) -> None:
        pass

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
