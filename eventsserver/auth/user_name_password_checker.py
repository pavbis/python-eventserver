from eventsserver.auth.auth_types import BasicAuthCredentials
from secrets import compare_digest


class ProvidesAuthorisationData:
    def get_user_accounts(self) -> [BasicAuthCredentials]:
        raise NotImplemented


class UsernamePasswordPermissionChecker:
    def __init__(self, auth_data: ProvidesAuthorisationData):
        self.__auth_data = auth_data

    def has_access(self, user_name: str, password: str) -> bool:
        if user_name == '' or compare_digest(password, ''):
            return False

        provided_credentials = BasicAuthCredentials.from_primitives(user_name, password)

        allowed_user = next(
            (allowed_user for allowed_user in self.__auth_data.get_user_accounts() if allowed_user.__eq__(provided_credentials)), None
        )

        return False if allowed_user is None else True
