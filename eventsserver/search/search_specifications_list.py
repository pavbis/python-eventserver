from eventsserver.search.specifications.period_specifications import *


class SearchSpecificationsList:
    def all_with_interval(self) -> [SpecifiesPeriod]:
        return (
            EmptyPeriodSpecification(),
            LastSixHoursSpecification(),
            LastDaySpecification(),
            LastTwoDaysSpecification(),
            LastWeekSpecification(),
            LastTwoWeeksSpecification(),
            LastMonthSpecification()
        )
