import unittest
import os
from pathlib import Path
from guesser.pavel_descriptor   import PavelDescriptor
from guesser.technology_guesser import TechnologyQuesser
from guesser.patrick_descriptor import PatrickDescriptor
from message.message_writer     import MessageWriter

class TechnologyQuesserTest(unittest.TestCase):
    
    def setUp(self):
        self.file_name      = 'test.txt'
        self.message_writer = MessageWriter(self.file_name)

    def get_file_content(self):
        return Path(self.file_name).read_text()

    def test_it_recognizes_pavel(self):
        descriptor = PavelDescriptor()
        result     = TechnologyQuesser(descriptor=descriptor, message_writer=self.message_writer).guess()

        self.assertTrue(os.path.isfile(self.file_name))
        self.assertEquals(PavelDescriptor.TECHNOLOGY, self.get_file_content())
        self.assertEqual(PavelDescriptor.TECHNOLOGY, result)

    def test_it_recognizes_patrick(self):
        descriptor = PatrickDescriptor()
        result     = TechnologyQuesser(descriptor=descriptor, message_writer=self.message_writer).guess()

        self.assertTrue(os.path.isfile(self.file_name))
        self.assertEquals(PatrickDescriptor.TECHNOLOGY, self.get_file_content())
        self.assertEqual(PatrickDescriptor.TECHNOLOGY, result)

    def tearDown(self):
        os.remove(self.file_name)


if __name__ == '__main__':
    unittest.main()