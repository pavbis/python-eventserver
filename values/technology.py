class InvalidTechnology(ValueError):
    """Throw this when technology is empty string."""

class Technology(object):
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidTechnology('technology can not not be empty.')
        self.primitive_value = primitive_value

    def __str__(self):
        return self.primitive_value
