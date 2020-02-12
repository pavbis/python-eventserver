from guesser.technology import Technology

class PavelDescriptor(object):

    TECHNOLOGY = 'PostgreSQL'

    def describe(self) -> Technology:
        return Technology(self.TECHNOLOGY)