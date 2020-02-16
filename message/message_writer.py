from contextlib import contextmanager
from values.file_name import FileName


class MessageWriter(object):
    def __init__(self, file_name: FileName):
        self.__file_name = file_name

    @contextmanager
    def open_file(self):
        try:
            file = open(str(self.__file_name), 'w')
            yield file
        finally:
            file.close()
