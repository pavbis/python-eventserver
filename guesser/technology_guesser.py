from values.technology import Technology
from message.message_writer import MessageWriter
from guesser.descriptors import DescribesTechnology

class TechnologyQuesser(object):
    def __init__(self, descriptor: DescribesTechnology, message_writer: MessageWriter):
        self.descriptor     = descriptor
        self.message_writer = message_writer

    def guess(self) -> Technology:
        message = self.descriptor.describe()

        with self.message_writer.open_file() as file: 
            file.write(str(message)) 

        return self.descriptor.describe()
