import uuid


class InvalidArgument(ValueError):
    """Throw argument is not valid."""


class StreamName(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('stream name can not not be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class ProducerId(object):
    def __init__(self, primitive_value):
        try:
            uuid.UUID(str(primitive_value))
        except ValueError:
            raise InvalidArgument('invalid uuid provided.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value
