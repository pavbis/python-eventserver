from unittest import TestCase
from eventsserver.auth.auth_types import Password, UserName, BasicAuthCredentials


class BaseCredentialsTest(TestCase):
    def test_it_can_be_created_from_primitives(self) -> None:
        primitive_user_name = 'foo'
        primitive_password = 'bar'

        basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, primitive_password)

        self.assertEqual(primitive_user_name, str(basic_auth_credentials.get_user_name()))
        self.assertEqual(primitive_password, str(basic_auth_credentials.get_password()))

    def test_it_can_be_created_over_normal_init(self) -> None:
        user_name = UserName('foo')
        password = Password('bar')

        base_auth_credentials = BasicAuthCredentials(user_name, password)

        self.assertEqual(str(user_name), str(base_auth_credentials.get_user_name()))
        self.assertEqual(str(password), str(base_auth_credentials.get_password()))

    def test_equal_returns_false_with_another_object_instance(self) -> None:
        primitive_user_name = 'foo'
        primitive_password = 'bar'

        basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, primitive_password)

        self.assertFalse(basic_auth_credentials.__eq__(UserName('invalid_object_instance')))

    def test_equal_returns_false_if_user_name_is_not_equal(self) -> None:
        primitive_user_name = 'foo'
        primitive_password = 'bar'

        basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, primitive_password)
        another_basic_auth_credentials = BasicAuthCredentials.from_primitives('test', primitive_password)

        self.assertFalse(basic_auth_credentials.__eq__(another_basic_auth_credentials))

    def test_equal_returns_false_if_password_is_not_equal(self) -> None:
        primitive_user_name = 'foo'
        primitive_password = 'bar'

        basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, primitive_password)
        another_basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, 'test')

        self.assertFalse(basic_auth_credentials.__eq__(another_basic_auth_credentials))

    def test_equal_returns_true_if_all_attributes_are_equal(self) -> None:
        primitive_user_name = 'foo'
        primitive_password = 'bar'

        basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, primitive_password)
        another_basic_auth_credentials = BasicAuthCredentials.from_primitives(primitive_user_name, primitive_password)

        self.assertTrue(basic_auth_credentials.__eq__(another_basic_auth_credentials))
