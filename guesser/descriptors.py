from values.technology import Technology


class DescribesTechnology(object):
    def describe(self) -> Technology:
        raise NotImplementedError


class PavelDescriptor(DescribesTechnology):
    TECHNOLOGY = 'PostgreSQL'

    def describe(self) -> Technology:
        return Technology(self.TECHNOLOGY)


class PatrickDescriptor(DescribesTechnology):
    TECHNOLOGY = 'AWS'

    def describe(self) -> Technology:
        return Technology(self.TECHNOLOGY)
