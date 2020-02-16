import pg8000
from eventsserver.config.parser import config
from eventsserver.storage.event_stores import PostgreSqlWriteEventStore
from eventsserver.value.objects import StreamName, ProducerId
import uuid


class DataBaseManager(object):
    __DATABASE_INI_FILE = 'eventsserver/config/database.ini'
    __SECTION = 'postgresql'

    def create_schema(self):
        connection_parameters = config(self.__DATABASE_INI_FILE, self.__SECTION)
        connection = pg8000.connect(**connection_parameters)

        stream_name = StreamName('pavel')
        producer_id = ProducerId(str(uuid.uuid4()))
        event_store = PostgreSqlWriteEventStore(connection)
        print(event_store.save_producer_stream_relation(producer_id, stream_name))
