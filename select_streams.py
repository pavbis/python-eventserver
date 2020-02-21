from eventsserver.storage.read_event_stores import PostgreSqlReadEventStore
from tests.support.rdbms.database_manager import DataBaseManager
from eventsserver.storage.expressions.select_streams_expressions import ProducerIdExpression
from eventsserver.storage.expressions.select_streams_expressions import SearchArgument
from eventsserver.readmodel.queryhandlers.find_streams_query_handler import FindStreamsQueryHandler
from eventsserver.readmodel.queries.find_streams_query import FindStreamsQuery

database_manager = DataBaseManager()
connection = database_manager.connection()
event_store = PostgreSqlReadEventStore(connection=connection)
expression = ProducerIdExpression(SearchArgument('f1f5cae6-30b7-43e7-a5e8-746a98bc265e'))
query = FindStreamsQuery(expression)
query_handler = FindStreamsQueryHandler(event_store)

result = query_handler.handle(query)

for stream in result.get_streams():
    print(str(stream.get_stream_name()))
