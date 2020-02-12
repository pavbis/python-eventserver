import unittest
import os
from pathlib import Path
from message.message_writer import MessageWriter

class MessageWriterTest(unittest.TestCase):
    def test_it_writes_content_into_provided_file(self):
        file_name       = 'message_writer.txt'
        message         = 'Test'
        message_writer  = MessageWriter(file_name)
        
        with message_writer.open_file() as file: 
            file.write(message) 

        self.assertTrue(os.path.isfile(file_name))
        self.assertEquals(message, Path(file_name).read_text())

        os.remove(file_name)