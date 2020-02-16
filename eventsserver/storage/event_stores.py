from typing import Optional

from eventsserver.value.objects import StreamName, ProducerId
from pg8000 import Connection


class PersistsEventStreams(object):
    def record_event(self) -> None:
        raise NotImplementedError

    def acknowledge_event(self) -> None:
        raise NotImplementedError

    def update_consumer_offset(self) -> None:
        raise NotImplementedError


class PostgreSqlWriteEventStore(PersistsEventStreams):
    def __init__(self, connection: Connection):
        self.connection = connection

    def record_event(self) -> None:
        pass

    def acknowledge_event(self) -> None:
        pass

    def update_consumer_offset(self) -> None:
        pass

    def save_producer_stream_relation(self, producer_id: ProducerId, stream_name: StreamName) -> None:

        query = 'INSERT INTO "producerStreamRelations" ("producerId", "streamName") VALUES (%s, %s) ON CONFLICT (' \
                '"streamName") DO NOTHING'

        cursor = self.connection.cursor()
        cursor.execute(query, [str(producer_id), str(stream_name)])
        self.connection.commit()

    def fetch_producer_id_for_stream_name(self, stream_name: StreamName) -> Optional[ProducerId]:
        with self.connection.cursor() as cursor:
            query = 'SELECT "producerId" FROM "producerStreamRelations" WHERE "streamName" = %s LIMIT 1'
            cursor.execute(query, [str(stream_name)])

            producer_id = cursor.fetchone()

            if producer_id is None:
                return producer_id
            else:
                return ProducerId(producer_id[0])
