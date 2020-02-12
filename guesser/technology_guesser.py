class TechnologyQuesser:
    def __init__(self, descriptor, message_writer):
        self.descriptor     = descriptor
        self.message_writer = message_writer

    def guess(self):
        message = self.descriptor.describe()

        with self.message_writer.open_file() as file: 
            file.write(message) 

        return self.descriptor.describe()
