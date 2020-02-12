import unittest
from values.technology import Technology, InvalidTechnology

class TechnologyTest(unittest.TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_empty(self):
        primitive_value = ''

        with self.assertRaises(InvalidTechnology) as context:
            Technology(primitive_value)
        self.assertTrue('technology can not not be empty.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = 'test'
        file_name = Technology(primitive_value)

        self.assertEquals(primitive_value, str(file_name))