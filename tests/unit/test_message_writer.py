from unittest import TestCase
import os
from pathlib import Path
from message.message_writer import MessageWriter
from values.file_name import FileName


class MessageWriterTest(TestCase):
    def test_it_writes_content_into_provided_file(self):
        file_name = FileName('message_writer.txt')
        message = 'Test'
        message_writer = MessageWriter(file_name)

        with message_writer.open_file() as file:
            file.write(message)

        self.assertTrue(os.path.isfile(str(file_name)))
        self.assertEqual(message, Path(str(file_name)).read_text())

        os.remove(str(file_name))
