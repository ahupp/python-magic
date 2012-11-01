
import os.path
import unittest
import random
import magic
from os import path


testfile = [
    ("magic.pyc", b"python 2.4 byte-compiled", b"application/octet-stream"),
    ("test.pdf", b"PDF document, version 1.2", b"application/pdf"),
    ("test.gz", b'gzip compressed data, was "test", from Unix, last modified: '
     b'Sat Jun 28 18:32:52 2008', b"application/x-gzip"),
    ("text.txt", b"ASCII text", b"text/plain"),
    # is there no better way to encode a unicode literal across python2/3.[01]/3.3?
    (b"\xce\xbb".decode('utf-8'), b"empty", b"application/x-empty")
    ]

testFileEncoding = [('text-iso8859-1.txt', b'iso-8859-1')]

class TestMagic(unittest.TestCase):

    mime = False
    
    def setUp(self):
        self.m = magic.Magic(mime=self.mime)

    def testFileTypes(self):
        for filename, desc, mime in testfile:
            filename = path.join(path.dirname(__file__),
                                 "testdata",
                                 filename)
            if self.mime:
                target = mime
            else:
                target = desc
                
            self.assertEqual(target, self.m.from_buffer(open(filename, 'rb').read(1024)))
            self.assertEqual(target, self.m.from_file(filename), filename)
        

    def testErrors(self):
        self.assertRaises(IOError, self.m.from_file, "nonexistent")
        self.assertRaises(magic.MagicException, magic.Magic, magic_file="noneexistent")
        os.environ['MAGIC'] = '/nonexistetn'
        self.assertRaises(magic.MagicException, magic.Magic)
        del os.environ['MAGIC']

class TestMagicMime(TestMagic):
    mime = True

class TestMagicMimeEncoding(unittest.TestCase):
    def setUp(self):
        self.m = magic.Magic(mime_encoding=True)

    def testFileEncoding(self):
        for filename, encoding in testFileEncoding:
            filename = path.join(path.dirname(__file__),
                                 "testdata",
                                 filename)
            self.assertEqual(encoding, self.m.from_buffer(open(filename, 'rb').read(1024)))
            self.assertEqual(encoding, self.m.from_file(filename), filename)


if __name__ == '__main__':
    unittest.main()
    
