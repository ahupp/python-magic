"""
Retro-compatibility tests
"""

import os
import unittest
import magic

from ._test_data import TEST_DATA_DIR, MagicTestCaseMixin, TEST_FILES


# testfile = [
#     # is there no better way to encode a unicode literal across
#     # python2/3.[01]/3.3?
#     (b"\xce\xbb".decode('utf-8'), b"empty", b"application/x-empty") ## <--???
# ]

testfile = []
testFileEncoding = []
for key, val in TEST_FILES.items():
    testfile.append((key, val[2], val[0]))
    testFileEncoding.append((key, val[1]))


class TestMagic(MagicTestCaseMixin, unittest.TestCase):
    def test_file_types(self):
        m = magic.Magic(mime=False)
        for filename, desc, mime in testfile:
            filename = os.path.join(TEST_DATA_DIR, filename)
            target = desc

            _from_buffer = m.from_buffer(open(filename, 'rb').read(1024))
            _from_file = m.from_file(filename)

            self.assertMatches(_from_buffer, target)
            self.assertMatches(_from_file, target)

    def test_file_types_mime(self):
        m = magic.Magic(mime=True)
        for filename, desc, mime in testfile:
            filename = os.path.join(TEST_DATA_DIR, filename)
            target = mime

            _from_buffer = m.from_buffer(open(filename, 'rb').read(1024))
            _from_file = m.from_file(filename)

            self.assertMatches(_from_buffer, target)
            self.assertMatches(_from_file, target)

    def test_errors(self):
        m = magic.Magic(mime=False)
        self.assertRaises(IOError, m.from_file, "nonexistent")
        self.assertRaises(
            magic.MagicException,
            magic.Magic,
            magic_file="noneexistent")
        os.environ['MAGIC'] = '/nonexistetn'
        self.assertRaises(magic.MagicException, magic.Magic)
        del os.environ['MAGIC']

    def test_errors_mime(self):
        m = magic.Magic(mime=True)
        self.assertRaises(IOError, m.from_file, "nonexistent")
        self.assertRaises(
            magic.MagicException,
            magic.Magic,
            magic_file="noneexistent")
        os.environ['MAGIC'] = '/nonexistetn'
        self.assertRaises(magic.MagicException, magic.Magic)
        del os.environ['MAGIC']

    def test_file_encoding(self):
        m = magic.Magic(mime_encoding=True)

        for filename, encoding in testFileEncoding:
            filename = os.path.join(TEST_DATA_DIR, filename)

            _from_buffer = m.from_buffer(open(filename, 'rb').read(1024))
            _from_file = m.from_file(filename)

            self.assertMatches(_from_buffer, encoding)
            self.assertMatches(_from_file, encoding)

    def test_old_from_buffer(self):
        for key, val in TEST_FILES.items():
            file_path = os.path.join(TEST_DATA_DIR, key)
            with open(file_path) as f:
                buf = f.read(1024)
            self.assertMatches(magic.from_buffer(buf, mime=False), val[2])
            self.assertMatches(magic.from_buffer(buf, mime=True), val[0])

    def test_old_from_file(self):
        for key, val in TEST_FILES.items():
            file_path = os.path.join(TEST_DATA_DIR, key)
            self.assertMatches(magic.from_file(file_path, mime=False), val[2])
            self.assertMatches(magic.from_file(file_path, mime=True), val[0])
