import os
# for output which reports a local time
os.environ['TZ'] = 'GMT'
import shutil
import os.path
import unittest

import magic


class MagicTest(unittest.TestCase):
    TESTDATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')

    def assert_values(self, m, expected_values, buf_equals_file=True):
        for filename, expected_value in expected_values.items():
            try:
                filename = os.path.join(self.TESTDATA_DIR, filename)
            except TypeError:
                filename = os.path.join(
                    self.TESTDATA_DIR.encode('utf-8'), filename)

            if type(expected_value) is not tuple:
                expected_value = (expected_value,)

            with open(filename, 'rb') as f:
                buf_value = m.from_buffer(f.read())

            file_value = m.from_file(filename)

            if buf_equals_file:
                self.assertEqual(buf_value, file_value)

            for value in (buf_value, file_value):
                self.assertIn(value, expected_value)

    def test_from_file_str_and_bytes(self):
        filename = os.path.join(self.TESTDATA_DIR, "test.pdf")

        self.assertEqual('application/pdf',
                         magic.from_file(filename, mime=True))
        self.assertEqual('application/pdf',
                         magic.from_file(filename.encode('utf-8'), mime=True))

    def test_from_buffer_str_and_bytes(self):
        m = magic.Magic(mime=True)
        s = '#!/usr/bin/env python\nprint("foo")'
        self.assertEqual("text/x-python", m.from_buffer(s))
        b = b'#!/usr/bin/env python\nprint("foo")'
        self.assertEqual("text/x-python", m.from_buffer(b))

    def test_mime_types(self):
        dest = os.path.join(MagicTest.TESTDATA_DIR,
                            b'\xce\xbb'.decode('utf-8'))
        shutil.copyfile(os.path.join(MagicTest.TESTDATA_DIR, 'lambda'), dest)
        try:
            m = magic.Magic(mime=True)
            self.assert_values(m, {
                'magic._pyc_': 'application/octet-stream',
                'test.pdf': 'application/pdf',
                'test.gz': ('application/gzip', 'application/x-gzip'),
                'text.txt': 'text/plain',
                b'\xce\xbb'.decode('utf-8'): 'text/plain',
                b'\xce\xbb': 'text/plain',
            })
        finally:
            os.unlink(dest)

    def test_descriptions(self):
        m = magic.Magic()
        os.environ['TZ'] = 'UTC'  # To get last modified date of test.gz in UTC
        try:
            self.assert_values(m, {
                'magic._pyc_': 'python 2.4 byte-compiled',
                'test.pdf': 'PDF document, version 1.2',
                'test.gz':
                ('gzip compressed data, was "test", from Unix, last '
                 'modified: Sun Jun 29 01:32:52 2008',
                 'gzip compressed data, was "test", last modified'
                 ': Sun Jun 29 01:32:52 2008, from Unix',
                 'gzip compressed data, was "test", last modified'
                 ': Sun Jun 29 01:32:52 2008, from Unix, original size 15'),
                'text.txt': 'ASCII text',
            }, buf_equals_file=False)
        finally:
            del os.environ['TZ']

    def test_unicode_result_nonraw(self):
        m = magic.Magic(raw=False)
        src = os.path.join(MagicTest.TESTDATA_DIR, 'pgpunicode')
        result = m.from_file(src)
        # NOTE: This check is added as otherwise some magic files don't identify the test case as a PGP key.
        if 'PGP' in result:
            assert r"PGP\011Secret Sub-key -" == result
        else:
            raise unittest.SkipTest("Magic file doesn't return expected type.")

    def test_unicode_result_raw(self):
        m = magic.Magic(raw=True)
        src = os.path.join(MagicTest.TESTDATA_DIR, 'pgpunicode')
        result = m.from_file(src)
        if 'PGP' in result:
            assert b'PGP\tSecret Sub-key -' == result.encode('utf-8')
        else:
            raise unittest.SkipTest("Magic file doesn't return expected type.")

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
        self.assertEqual(m.from_file(filename), 'image/jpeg')

        m = magic.Magic(mime=True, keep_going=True)
        self.assertEqual(m.from_file(filename),
                         'image/jpeg\\012- application/octet-stream')

    def test_rethrow(self):
        old = magic.magic_buffer
        try:
            def t(x, y):
                raise magic.MagicException("passthrough")
            magic.magic_buffer = t

            with self.assertRaises(magic.MagicException):
                magic.from_buffer("hello", True)
        finally:
            magic.magic_buffer = old

    def test_getparam(self):
        m = magic.Magic(mime=True)
        m.setparam(magic.MAGIC_PARAM_INDIR_MAX, 1)
        self.assertEqual(m.getparam(magic.MAGIC_PARAM_INDIR_MAX), 1)

if __name__ == '__main__':
    unittest.main()
