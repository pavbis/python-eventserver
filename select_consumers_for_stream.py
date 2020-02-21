from eventsserver.storage.read_event_stores import PostgreSqlReadEventStore
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.value.objects import StreamName

database_manager = DataBaseManager()
connection = database_manager.connection()
stream_name = StreamName('nicowa')
event_store = PostgreSqlReadEventStore(connection)
consumers = event_store.select_consumers_for_stream(stream_name)

for consumer in consumers:
    print(str(consumer.get_consumer_id()))

