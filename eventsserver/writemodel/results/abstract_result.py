from eventsserver.writemodel.constants.result_type import ResultType


class AbstractResult(object):
    def __init__(self, result_type=ResultType.SUCCESS, message=''):
        self.__result_type = result_type
        self.__message = message

    def succeeded(self) -> bool:
        return ResultType.SUCCESS == self.__result_type

    def failure(self) -> bool:
        return ResultType.FAILURE == self.__result_type

    def get_message(self) -> str:
        return self.__message
