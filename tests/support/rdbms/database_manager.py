import pg8000
from eventsserver.config.parser import config
from eventsserver.storage.event_stores import PostgreSqlWriteEventStore
from eventsserver.value.objects import StreamName, ProducerId, EventName, EventId
from eventsserver.value.event import Event
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
        event_id = EventId(str(uuid.uuid4()))
        event_name = EventName('scream')
        event = Event(event_id, event_name)

