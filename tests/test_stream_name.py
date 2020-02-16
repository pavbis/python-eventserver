from unittest import TestCase
from eventsserver.value.objects import StreamName, InvalidArgument


class StreamNameTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidArgument) as context:
            StreamName(primitive_value)
        self.assertTrue('stream name can not not be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test'
        file_name = StreamName(primitive_value)

        self.assertEqual(primitive_value, str(file_name))
