from eventsserver.storage.expressions.select_streams_expressions import ProvidesPredicate


class FindStreamsQuery(object):
    def __init__(self, expression: ProvidesPredicate):
        self.__expression = expression

    def get_expression(self) -> ProvidesPredicate:
        return self.__expression
