from eventsserver.storage.read_event_stores import PostgreSqlReadEventStore
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.readmodel.queries.find_events_query import FindEventsQuery
from eventsserver.value.objects import ConsumerId, StreamName, EventName, MaxEventCount

database_manager = DataBaseManager()
connection = database_manager.connection()
event_store = PostgreSqlReadEventStore(connection=connection)

query = FindEventsQuery(
    consumer_id=ConsumerId('2480b859-e08a-4414-9c7d-003bc1a4b444'),
    stream_name=StreamName('nicowa'),
    event_name=EventName('Snickers'),
    max_event_count=MaxEventCount(50)
)

events = event_store.select_events(query=query)

for event in events:
    print(str(event.event_id))
