import os.path
import unittest

import magic


class MagicTest(unittest.TestCase):
    TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'testdata')

    def assert_values(self, m, expected_values):
        for filename, expected_value in expected_values.items():
            filename = os.path.join(self.TESTDATA_DIR, filename)

            with open(filename, 'rb') as f:
                value = m.from_buffer(f.read())
            self.assertEqual(value, expected_value)

            value = m.from_file(filename)
            self.assertEqual(value, expected_value)

    def test_mime_types(self):
        m = magic.Magic(mime=True)
        self.assert_values(m, {
            'magic.pyc': b'application/octet-stream',
            'test.pdf': b'application/pdf',
            'test.gz': b'application/x-gzip',
            'text.txt': b'text/plain',
        })

    def test_descriptions(self):
        m = magic.Magic()
        os.environ['TZ'] = 'UTC'  # To get the last modified date of test.gz in UTC
        try:
            self.assert_values(m, {
                'magic.pyc': b'python 2.4 byte-compiled',
                'test.pdf': b'PDF document, version 1.2',
                'test.gz': b'gzip compressed data, was "test", from Unix, '
                           b'last modified: Sun Jun 29 01:32:52 2008',
                'text.txt': b'ASCII text',
            })
        finally:
            del os.environ['TZ']

    def test_mime_encodings(self):
        m = magic.Magic(mime_encoding=True)
        self.assert_values(m, {
            'text-iso8859-1.txt': b'iso-8859-1',
            'text.txt': b'us-ascii',
        })

    def test_errors(self):
        m = magic.Magic()
        self.assertRaises(IOError, m.from_file, 'nonexistent')
        self.assertRaises(magic.MagicException, magic.Magic,
                          magic_file='nonexistent')
        os.environ['MAGIC'] = 'nonexistent'
        try:
            self.assertRaises(magic.MagicException, magic.Magic)
        finally:
            del os.environ['MAGIC']


if __name__ == '__main__':
    unittest.main()
