import unittest
import os
from pathlib import Path
from guesser.descriptors import PavelDescriptor, PatrickDescriptor
from guesser.technology_guesser import TechnologyQuesser
from values.technology import Technology
from message.message_writer import MessageWriter
from values.file_name import FileName


class TechnologyQuesserTest(unittest.TestCase):

    def setUp(self):
        self.file_name = FileName('test.txt')
        self.message_writer = MessageWriter(self.file_name)

    def get_file_content(self):
        return Path(str(self.file_name)).read_text()

    def test_it_recognizes_pavel(self):
        descriptor = PavelDescriptor()
        result = TechnologyQuesser(descriptor=descriptor, message_writer=self.message_writer).guess()

        self.assertTrue(os.path.isfile(str(self.file_name)))
        self.assertEqual(PavelDescriptor.TECHNOLOGY, self.get_file_content())
        self.assertIsInstance(result, Technology)
        self.assertEqual(PavelDescriptor.TECHNOLOGY, str(result))

    def test_it_recognizes_patrick(self):
        descriptor = PatrickDescriptor()
        result = TechnologyQuesser(descriptor=descriptor, message_writer=self.message_writer).guess()

        self.assertTrue(os.path.isfile(str(self.file_name)))
        self.assertEqual(PatrickDescriptor.TECHNOLOGY, self.get_file_content())
        self.assertIsInstance(result, Technology)
        self.assertEqual(PatrickDescriptor.TECHNOLOGY, str(result))

    def tearDown(self):
        os.remove(str(self.file_name))


if __name__ == '__main__':
    unittest.main()
