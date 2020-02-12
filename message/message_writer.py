from contextlib import contextmanager
from message.file_name import FileName

class MessageWriter(object):
    def __init__(self, file_name: FileName):
        self.file_name = file_name

    @contextmanager 
    def open_file(self):
        try:
            file = open(str(self.file_name), 'w')
            yield file
        finally:
            file.close()

        