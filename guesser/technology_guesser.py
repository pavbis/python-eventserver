class TechnologyQuesser:
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def guess(self):
        return self.descriptor.describe()
