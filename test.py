
import os.path
import unittest
import random
from StringIO import StringIO
from os import path
from magic import Magic, MagicException

testfile = [
    ("magic.pyc", "python 2.4 byte-compiled", "application/octet-stream"),
    ("test.pdf", "PDF document, version 1.2", "application/pdf"),
    ("test.gz", 'gzip compressed data, was "test", from Unix, last modified: '
     'Sat Jun 28 18:32:52 2008', "application/x-gzip"),
    ("text.txt", "ASCII text", "text/plain"),
    ]

testFileEncoding = [('text-iso8859-1.txt', 'iso-8859-1')]

class TestMagic(unittest.TestCase):

    mime = False
    
    def setUp(self):
        self.m = Magic(mime=self.mime)

    def testFileTypes(self):
        for filename, desc, mime in testfile:
            filename = path.join(path.dirname(__file__),
                                 "testdata",
                                 filename)
            if self.mime:
                target = mime
            else:
                target = desc
                
            self.assertEqual(target, self.m.from_buffer(open(filename).read(1024)))
            self.assertEqual(target, self.m.from_file(filename), filename)
        

    def testErrors(self):
        self.assertRaises(IOError, self.m.from_file, "nonexistent")
        self.assertRaises(MagicException, Magic, magic_file="noneexistent")
        os.environ['MAGIC'] = '/nonexistetn'
        self.assertRaises(MagicException, Magic)
        del os.environ['MAGIC']

class TestMagicMime(TestMagic):
    mime = True

class TestMagicMimeEncoding(unittest.TestCase):
    def setUp(self):
        self.m = Magic(mime_encoding=True)

    def testFileEncoding(self):
        for filename, encoding in testFileEncoding:
            filename = path.join(path.dirname(__file__),
                                 "testdata",
                                 filename)
            self.assertEqual(encoding, self.m.from_buffer(open(filename).read(1024)))
            self.assertEqual(encoding, self.m.from_file(filename), filename)


if __name__ == '__main__':
    unittest.main()
    
