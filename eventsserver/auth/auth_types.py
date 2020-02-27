from eventsserver.value.objects import InvalidArgument


class UserName:
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('User name cannot be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class Password:
    def __init__(self, primitive_value: str):
        if not primitive_value:
            raise InvalidArgument('Password cannot be empty.')
        self.__primitive_value = primitive_value

    def __str__(self) -> str:
        return self.__primitive_value


class BasicAuthCredentials:
    def __init__(self, user_name: UserName, password: Password):
        self.__user_name = user_name
        self.__password = password

    @classmethod
    def from_primitives(cls, user_name: str, password: str):
        instance = cls.__new__(cls)

        instance.__user_name = UserName(user_name)
        instance.__password = Password(password)

        return instance

    def get_user_name(self) -> UserName:
        return self.__user_name

    def get_password(self) -> Password:
        return self.__password

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return str(self.__user_name) == str(other.__user_name) and str(self.__password) == str(other.__password)
