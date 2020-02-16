from values.technology import Technology
from message.message_writer import MessageWriter
from guesser.descriptors import DescribesTechnology


class TechnologyQuesser(object):
    def __init__(self, descriptor: DescribesTechnology, message_writer: MessageWriter):
        self.__descriptor = descriptor
        self.__message_writer = message_writer

    def guess(self) -> Technology:
        message = self.__descriptor.describe()

        with self.__message_writer.open_file() as file:
            file.write(str(message))

        return self.__descriptor.describe()
