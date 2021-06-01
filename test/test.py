import os

# for output which reports a local time
os.environ['TZ'] = 'GMT'

if os.environ.get('LC_ALL', '') != 'en_US.UTF-8':
    # this ensure we're in a utf-8 default filesystem encoding which is
    # necessary for some tests
    raise Exception("must run `export LC_ALL=en_US.UTF-8` before running test suite")

import shutil
import os.path
import unittest

import magic
import sys

# magic_descriptor is broken (?) in centos 7, so don't run those tests
SKIP_FROM_DESCRIPTOR = bool(os.environ.get('SKIP_FROM_DESCRIPTOR'))

class MagicTest(unittest.TestCase):
    TESTDATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')

    def test_version(self):
        try:
            self.assertTrue(magic.version() > 0)
        except NotImplementedError:
            pass

    def test_fs_encoding(self):
        self.assertEqual('utf-8', sys.getfilesystemencoding().lower())

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

    def test_from_descriptor_str_and_bytes(self):
        if SKIP_FROM_DESCRIPTOR:
            self.skipTest("magic_descriptor is broken in this version of libmagic")

        filename = os.path.join(self.TESTDATA_DIR, "test.pdf")
        with open(filename) as f:
            self.assertEqual('application/pdf',
                             magic.from_descriptor(f.fileno(), mime=True))
            self.assertEqual('application/pdf',
                             magic.from_descriptor(f.fileno(), mime=True))

    def test_from_buffer_str_and_bytes(self):
        if SKIP_FROM_DESCRIPTOR:
            self.skipTest("magic_descriptor is broken in this version of libmagic")
        m = magic.Magic(mime=True)

        self.assertTrue(
            m.from_buffer('#!/usr/bin/env python\nprint("foo")')
            in ("text/x-python", "text/x-script.python"))
        self.assertTrue(
            m.from_buffer(b'#!/usr/bin/env python\nprint("foo")')
            in ("text/x-python", "text/x-script.python"))

    def test_mime_types(self):
        dest = os.path.join(MagicTest.TESTDATA_DIR,
                            b'\xce\xbb'.decode('utf-8'))
        shutil.copyfile(os.path.join(MagicTest.TESTDATA_DIR, 'lambda'), dest)
        try:
            m = magic.Magic(mime=True)
            self.assert_values(m, {
                'magic._pyc_': ('application/octet-stream', 'text/x-bytecode.python'),
                'test.pdf': 'application/pdf',
                'test.gz': ('application/gzip', 'application/x-gzip'),
                'test.snappy.parquet': 'application/octet-stream',
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
                'test.pdf': ('PDF document, version 1.2',
                             'PDF document, version 1.2, 2 pages'),
                'test.gz':
                    ('gzip compressed data, was "test", from Unix, last '
                     'modified: Sun Jun 29 01:32:52 2008',
                     'gzip compressed data, was "test", last modified'
                     ': Sun Jun 29 01:32:52 2008, from Unix',
                     'gzip compressed data, was "test", last modified'
                     ': Sun Jun 29 01:32:52 2008, from Unix, original size 15',
                     'gzip compressed data, was "test", '
                     'last modified: Sun Jun 29 01:32:52 2008, '
                     'from Unix, original size modulo 2^32 15',
                     'gzip compressed data, was "test", last modified'
                     ': Sun Jun 29 01:32:52 2008, from Unix, truncated'
                     ),
                'text.txt': 'ASCII text',
                'test.snappy.parquet': ('Apache Parquet', 'Par archive data'),
            }, buf_equals_file=False)
        finally:
            del os.environ['TZ']

    def test_extension(self):
        try:
            m = magic.Magic(extension=True)
            self.assert_values(m, {
                # some versions return '' for the extensions of a gz file,
                # including w/ the command line.  Who knows...
                'test.gz': ('gz/tgz/tpz/zabw/svgz', '', '???'),
                'name_use.jpg': 'jpeg/jpg/jpe/jfif',
            })
        except NotImplementedError:
            self.skipTest('MAGIC_EXTENSION not supported in this version')

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

        try:
            # this will throw if you have an "old" version of the library
            # I'm otherwise not sure how to query if keep_going is supported
            magic.version()
            m = magic.Magic(mime=True, keep_going=True)
            self.assertEqual(m.from_file(filename),
                             'image/jpeg\\012- application/octet-stream')
        except NotImplementedError:
            pass

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
        try:
            m.setparam(magic.MAGIC_PARAM_INDIR_MAX, 1)
            self.assertEqual(m.getparam(magic.MAGIC_PARAM_INDIR_MAX), 1)
        except NotImplementedError:
            pass

    def test_name_count(self):
        m = magic.Magic()
        with open(os.path.join(self.TESTDATA_DIR, 'name_use.jpg'), 'rb') as f:
            m.from_buffer(f.read())


if __name__ == '__main__':
    unittest.main()
