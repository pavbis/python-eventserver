from eventsserver.storage.read_event_stores import PostgreSqlReadEventStore
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.value.objects import EventId
from eventsserver.readmodel.queries.read_event_payload_query import ReadEventPayloadQuery
from eventsserver.readmodel.queryhandlers.read_event_payload_query_handler import ReadEventPayloadQueryHandler

database_manager = DataBaseManager()
connection = database_manager.connection()
event_store = PostgreSqlReadEventStore(connection=connection)
event_id = EventId('ebf1e616-ca51-4f76-908d-d5781c0ad550')
query = ReadEventPayloadQuery(event_id)
query_handler = ReadEventPayloadQueryHandler(event_store)

result = query_handler.handle(query)

print(str(result.get_event_json()))
