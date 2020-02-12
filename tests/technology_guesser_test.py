import unittest
from guesser.pavel_descriptor   import PavelDescriptor
from guesser.technology_guesser import TechnologyQuesser
from guesser.patrick_descriptor import PatrickDescriptor

class TechnologyQuesserTest(unittest.TestCase):
    
    def setUp(self):
        self.pavel_descriptor = PavelDescriptor()
        self.pavel_result     = TechnologyQuesser(descriptor=self.pavel_descriptor).guess()

        self.patrick_descriptor = PatrickDescriptor()
        self.patrick_result     = TechnologyQuesser(descriptor=self.patrick_descriptor).guess()

    def test_it_recognizes_pavel(self):
        self.assertEqual('PostgreSQL', self.pavel_result)

    def test_it_recognizes_patrick(self):
        self.assertEqual('AWS', self.patrick_result)


if __name__ == '__main__':
    unittest.main()