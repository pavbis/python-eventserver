import unittest
from message.file_name import FileName, InvalidFileName

class FileNameTest(unittest.TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidFileName) as error:
            FileName(primitive_value)
        self.assertEqual(str(error.exception), 'file name can not not be empty.')

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test.txt'
        file_name = FileName(primitive_value)

        self.assertEquals(primitive_value, str(file_name))
