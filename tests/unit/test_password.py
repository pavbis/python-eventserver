from unittest import TestCase
from eventsserver.value.objects import InvalidArgument
from eventsserver.auth.auth_types import Password


class PasswordTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self) -> None:
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            Password(primitive_value)
        self.assertTrue('Password cannot be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self) -> None:
        primitive_value = 'test'
        password = Password(primitive_value)

        self.assertEqual(primitive_value, str(password))
