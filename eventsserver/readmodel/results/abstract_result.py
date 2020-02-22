from eventsserver.readmodel.constants.result_type import ResultType


class AbstractResult:
    def __init__(self, result_type: int = ResultType.SUCCESS, message: str = ''):
        self.__result_type = result_type
        self.__message = message

    def succeeded(self) -> bool:
        return ResultType.SUCCESS == self.__result_type

    def failure(self) -> bool:
        return ResultType.FAILURE == self.__result_type

    def get_message(self) -> str:
        return self.__message
