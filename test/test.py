import os
# for output which reports a local time
os.environ['TZ'] = 'GMT'
import shutil
import os.path
import unittest

import magic

class MagicTest(unittest.TestCase):
    TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'testdata')

    def assert_values(self, m, expected_values):
        for filename, expected_value in expected_values.items():
            try:
                filename = os.path.join(self.TESTDATA_DIR, filename)
            except TypeError:
                filename = os.path.join(self.TESTDATA_DIR.encode('utf-8'), filename)

            with open(filename, 'rb') as f:
                value = m.from_buffer(f.read())
                expected_value_bytes = expected_value.encode('utf-8')
                self.assertEqual(value, expected_value_bytes)

            value = m.from_file(filename)
            self.assertEqual(value, expected_value_bytes)
        
    def test_mime_types(self):
        dest = os.path.join(MagicTest.TESTDATA_DIR, b'\xce\xbb'.decode('utf-8'))
        shutil.copyfile(os.path.join(MagicTest.TESTDATA_DIR, 'lambda'), dest)
        try:
            m = magic.Magic(mime=True)
            self.assert_values(m, {
                'magic.pyc': 'application/octet-stream',
                'test.pdf': 'application/pdf',
                'test.gz': 'application/gzip',
                'text.txt': 'text/plain',
                b'\xce\xbb'.decode('utf-8'): 'text/plain',
                b'\xce\xbb': 'text/plain',
            })
        finally:
            os.unlink(dest)

    def test_descriptions(self):
        m = magic.Magic()
        os.environ['TZ'] = 'UTC'  # To get the last modified date of test.gz in UTC
        try:
            self.assert_values(m, {
                'magic.pyc': 'python 2.4 byte-compiled',
                'test.pdf': 'PDF document, version 1.2',
                'test.gz':
                'gzip compressed data, was "test", last modified: Sun Jun 29 01:32:52 2008, from Unix',
                'text.txt': 'ASCII text',
            })
        finally:
            del os.environ['TZ']

    def test_mime_encodings(self):
        m = magic.Magic(mime_encoding=True)
        self.assert_values(m, {
            'text-iso8859-1.txt': 'iso-8859-1',
            'text.txt': 'us-ascii',
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

    def test_keep_going(self):
        filename = os.path.join(self.TESTDATA_DIR, 'keep-going.jpg')

        m = magic.Magic(mime=True)
        self.assertEqual(m.from_file(filename), 
                         'image/jpeg'.encode('utf-8'))
        
        m = magic.Magic(mime=True, keep_going=True)
        self.assertEqual(m.from_file(filename), 'image/jpeg'.encode('utf-8'))

if __name__ == '__main__':
    unittest.main()
