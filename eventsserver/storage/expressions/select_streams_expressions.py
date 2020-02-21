from abc import ABC


class ContainsSearchCriteria(object):
    pass


class SearchArgument(ContainsSearchCriteria):
    def __init__(self, argument: str):
        self.__argument = argument

    def __str__(self) -> str:
        return self.__argument


class ProvidesPredicate(object):
    def predicate(self) -> str:
        raise NotImplementedError

    def search_criteria(self) -> ContainsSearchCriteria:
        raise NotImplementedError


class AbstractExpression(ProvidesPredicate, ABC):
    def __init__(self, search_criteria: ContainsSearchCriteria):
        self.__search_criteria = search_criteria

    def search_criteria(self) -> ContainsSearchCriteria:
        return self.__search_criteria


class ProducerIdExpression(AbstractExpression):
    def predicate(self) -> str:
        return 'WHERE "producerId" = \'%s\'' % str(self.search_criteria())


class StreamNameExpression(AbstractExpression):
    def predicate(self) -> str:
        return 'WHERE "streamName" IS NOT NULL'
