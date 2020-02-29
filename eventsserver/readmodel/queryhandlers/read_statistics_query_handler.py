from eventsserver.statistics.statistics_storages import ProvidesStatistics
from eventsserver.readmodel.results.statistics_data_result import StatisticsDataResult
from eventsserver.readmodel.constants.result_type import ResultType


class ReadStatisticsDataQueryHandler:
    def __init__(self, storage: ProvidesStatistics):
        self.__storage = storage

    def handle(self) -> StatisticsDataResult:
        try:
            event_chart_data = self.__storage.events_stats()
            stream_chart_data = self.__storage.stream_stats()
            stream_statistics_chart_data = self.__storage.streams_chart_stats()

            result = StatisticsDataResult()
            result.set_event_chart_data(event_chart_data)
            result.set_stream_chart_data(stream_chart_data)
            result.set_stream_statistics_chart_data(stream_statistics_chart_data)

            return result
        except Exception as error:
            return StatisticsDataResult(ResultType.FAILURE, str(error))
