from eventsserver.readmodel.results.abstract_result import AbstractResult
from eventsserver.value.objects import ProvidesAggregatedJson


class StatisticsDataResult(AbstractResult):
    __event_chart_data = None
    __stream_chart_data = None
    __stream_statistics_chart_data = None

    def get_event_chart_data(self) -> ProvidesAggregatedJson:
        return self.__event_chart_data

    def set_event_chart_data(self, event_data: ProvidesAggregatedJson) -> None:
        self.__event_chart_data = event_data

    def get_stream_chart_data(self) -> ProvidesAggregatedJson:
        return self.__stream_chart_data

    def set_stream_chart_data(self, stream_data: ProvidesAggregatedJson) -> None:
        self.__stream_chart_data = stream_data

    def get_stream_statistics_chart_data(self) -> ProvidesAggregatedJson:
        return self.__stream_statistics_chart_data

    def set_stream_statistics_chart_data(self, stream_data: ProvidesAggregatedJson) -> None:
        self.__stream_statistics_chart_data = stream_data
