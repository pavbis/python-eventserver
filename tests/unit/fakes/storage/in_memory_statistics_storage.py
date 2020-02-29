from psycopg2 import DatabaseError
from eventsserver.statistics.statistics_storages import ProvidesStatistics
from eventsserver.value.objects import ProvidesAggregatedJson
from eventsserver.value.objects import AggregatedJson


class InMemoryStatisticsStorage(ProvidesStatistics):
    STATISTICS_STORAGE_ERROR = 'stats error'

    __will_raise_database_error = False

    def will_raise_database_error(self) -> None:
        self.__will_raise_database_error = True

    def reset(self):
        self.__will_raise_database_error = False

    def events_stats(self) -> ProvidesAggregatedJson:
        if self.__will_raise_database_error:
            raise DatabaseError(self.STATISTICS_STORAGE_ERROR)

        return AggregatedJson('{"foo": "bar"}')

    def stream_stats(self) -> ProvidesAggregatedJson:
        return AggregatedJson('{"foo": "bar"}')

    def streams_chart_stats(self) -> ProvidesAggregatedJson:
        return AggregatedJson('{"foo": "bar"}')