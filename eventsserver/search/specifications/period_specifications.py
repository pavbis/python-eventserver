from eventsserver.value.objects import Period, DateRange


class SpecifiesPeriod:
    def is_satisfied_by(self, period: Period) -> bool:
        raise NotImplementedError

    def and_expression(self) -> str:
        raise NotImplementedError

    def period(self) -> str:
        raise NotImplementedError

    def period_literal(self) -> str:
        raise NotImplementedError

    def get_instance(self, period: Period):
        if self.is_satisfied_by(period):
            return None
        else:
            return self


class DateRangeSpecification(SpecifiesPeriod):
    def __init__(self, date_range: DateRange):
        self.__date_range = date_range

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__date_range.is_valid()

    def and_expression(self) -> str:
        return 'AND "createdAt" BETWEEN \'{}\' AND \'{}\''.format(
            self.__date_range.get_start().strftime('%Y-%m-%d 00:00:00'),
            self.__date_range.get_end().strftime('%Y-%m-%d 23:59:59')
        )

    def period(self) -> str:
        return ''

    def period_literal(self) -> str:
        return ''


class EmptyPeriodSpecification(SpecifiesPeriod):
    def is_satisfied_by(self, period: Period) -> bool:
        return '' == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" IS NOT NULL';

    def period(self) -> str:
        return ''

    def period_literal(self) -> str:
        return 'Choose'


class LastDaySpecification(SpecifiesPeriod):
    __period_string = '24 hour'
    __period_literal = 'Last 24 hours'

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__period_string == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" >= now() - interval \'{}\''.format(self.__period_string)

    def period(self) -> str:
        return self.__period_string

    def period_literal(self) -> str:
        return self.__period_literal


class LastMonthSpecification(SpecifiesPeriod):
    __period_string = '1 month'
    __period_literal = 'Last month'

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__period_string == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" >= now() - interval \'{}\''.format(self.__period_string)

    def period(self) -> str:
        return self.__period_string

    def period_literal(self) -> str:
        return self.__period_literal


class LastSixHoursSpecification(SpecifiesPeriod):
    __period_string = '6 hour'
    __period_literal = 'Last 6 hours'

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__period_string == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" >= now() - interval \'{}\''.format(self.__period_string)

    def period(self) -> str:
        return self.__period_string

    def period_literal(self) -> str:
        return self.__period_literal


class LastTwoDaysSpecification(SpecifiesPeriod):
    __period_string = '2 day'
    __period_literal = 'Last 2 days'

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__period_string == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" >= now() - interval \'{}\''.format(self.__period_string)

    def period(self) -> str:
        return self.__period_string

    def period_literal(self) -> str:
        return self.__period_literal


class LastTwoWeeksSpecification(SpecifiesPeriod):
    __period_string = '14 day'
    __period_literal = 'Last 2 weeks'

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__period_string == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" >= now() - interval \'{}\''.format(self.__period_string)

    def period(self) -> str:
        return self.__period_string

    def period_literal(self) -> str:
        return self.__period_literal


class LastWeekSpecification(SpecifiesPeriod):
    __period_string = '7 day'
    __period_literal = 'Last 7 days'

    def is_satisfied_by(self, period: Period) -> bool:
        return self.__period_string == str(period)

    def and_expression(self) -> str:
        return 'AND "createdAt" >= now() - interval \'{}\''.format(self.__period_string)

    def period(self) -> str:
        return self.__period_string

    def period_literal(self) -> str:
        return self.__period_literal
