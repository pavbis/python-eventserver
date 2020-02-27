from unittest import TestCase
from eventsserver.auth.auth_types import BasicAuthCredentials
from eventsserver.auth.user_name_password_checker import UsernamePasswordPermissionChecker, ProvidesAuthorisationData


class FakeAutData(ProvidesAuthorisationData):
    def get_user_accounts(self) -> [BasicAuthCredentials]:
        return [BasicAuthCredentials.from_primitives('foo', 'bar')]


class USerNamePasswordCheckerTest(TestCase):
    def setUp(self) -> None:
        self.auth_data = FakeAutData()
        self.checker = UsernamePasswordPermissionChecker(self.auth_data)

    def test_it_returns_false_if_user_name_or_password_not_provided(self) -> None:
        self.assertFalse(self.checker.has_access('', 'bar'))
        self.assertFalse(self.checker.has_access('foo', ''))

    def test_it_returns_false_if_provided_credentials_are_not_valid(self) -> None:
        self.assertFalse(self.checker.has_access('foo', 'test'))
        self.assertFalse(self.checker.has_access('test', 'test'))
        self.assertFalse(self.checker.has_access('test', 'bar'))

    def test_it_returns_true_if_provided_credentials_are_valid(self) -> None:
        self.assertTrue(self.checker.has_access('foo', 'bar'))
