from guesser.technology import Technology

class PatrickDescriptor(object):

    TECHNOLOGY = 'AWS'

    def describe(self) -> Technology:
        return Technology(self.TECHNOLOGY)