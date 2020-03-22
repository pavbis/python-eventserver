from eventsserver.search.specifications.period_specifications import *
from eventsserver.value.objects import Period


class UnsupportedPeriod(ValueError):
    """Throw argument is not valid."""


class EventPeriodSearch:
    def __init__(self, specifications: [SpecifiesPeriod]):
        self.__specifications = specifications

    def find_specification(self, period: Period) -> SpecifiesPeriod:
        specification = next(
            (specification for specification in self.__specifications if specification.is_satisfied_by(period)), None
        )

        if specification is not None:
            return specification

        raise UnsupportedPeriod('Period "{}" is not supported or invalid.'.format(str(period)))
