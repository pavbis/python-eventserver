from eventsserver.storage.read_event_stores import PostgreSqlReadEventStore
from eventsserver.rdbms.connection import Connection
from eventsserver.value.objects import EventId
from eventsserver.readmodel.queries.read_event_payload_query import ReadEventPayloadQuery
from eventsserver.readmodel.queryhandlers.read_event_payload_query_handler import ReadEventPayloadQueryHandler
from eventsserver.statistics.statistics_storages import PostgreSqlStatisticsStorage

connection = Connection()
event_store = PostgreSqlReadEventStore(connection=connection)
event_id = EventId('ebf1e616-ca51-4f76-908d-d5781c0ad550')
query = ReadEventPayloadQuery(event_id)
query_handler = ReadEventPayloadQueryHandler(event_store)

result = query_handler.handle(query)

stats_store = PostgreSqlStatisticsStorage(connection)

print(str(result.get_event_json()))
