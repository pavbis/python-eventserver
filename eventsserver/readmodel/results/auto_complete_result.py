from eventsserver.readmodel.results.abstract_result import AbstractResult
from eventsserver.value.objects import ProvidesAggregatedJson


class AutoCompleteResult(AbstractResult):
    __aggregated_json = None

    def get_aggregated_json(self) -> ProvidesAggregatedJson:
        return self.__aggregated_json

    def set_aggregated_json(self, json: ProvidesAggregatedJson):
        self.__aggregated_json = json
