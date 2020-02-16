class InvalidFileName(ValueError):
    """Throw this when file name is empty string."""


class FileName(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidFileName('file name can not not be empty.')
        self.__primitive_value = primitive_value

    def __str__(self):
        return self.__primitive_value
