from unittest import TestCase
from eventsserver.rdbms.parser import *


class MyTestCase(TestCase):
    def test_it_raises_exception_if_section_does_not_exist(self):
        with self.assertRaises(InvalidConfigSection) as context:
            config('invalid.ini', 'foo')
        self.assertTrue('Section foo not found in the invalid.ini file' in str(context.exception))

    def test_it_returns_section_if_section_exists(self):

        self.assertEqual(
            config('eventsserver/rdbms/database.ini', 'postgresql'),
            {
                'database': 'python_test',
                'host': 'postgres',
                'password': 'root',
                'user': 'root'
            }
        )

