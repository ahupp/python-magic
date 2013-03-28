"""
Test cases for the wrapped C library.
"""

import os
import unittest
from magic.wrapper import magic_open, magic_load, magic_file, MAGIC_MIME, \
    MAGIC_MIME_ENCODING, MAGIC_COMPRESS, MAGIC_NONE, MAGIC_MIME_TYPE
from ._test_data import TEST_DATA_DIR, TEST_FILES, TEST_FILES_COMPRESSED, MagicTestCaseMixin


class TestMagicWrapped(MagicTestCaseMixin, unittest.TestCase):
    def test_files(self):
        cookie_desc = magic_open(MAGIC_NONE)
        cookie_mime = magic_open(MAGIC_MIME_TYPE)
        cookie_charset = magic_open(MAGIC_MIME_ENCODING)
        cookie_mime_full = magic_open(MAGIC_MIME)

        magic_load(cookie_desc)
        magic_load(cookie_mime)
        magic_load(cookie_charset)
        magic_load(cookie_mime_full)

        for filename in sorted(TEST_FILES.keys()):
            mime, charset, desc, mime_charset = TEST_FILES[filename]

            file_path = os.path.join(TEST_DATA_DIR, filename)

            read_desc = magic_file(cookie_desc, file_path)
            read_mime = magic_file(cookie_mime, file_path)
            read_charset = magic_file(cookie_charset, file_path)
            read_mime_full = magic_file(cookie_mime_full, file_path)

            self.assertMatches(read_mime, mime)
            self.assertMatches(read_mime_full, mime_charset)
            self.assertMatches(read_charset, charset)
            self.assertMatches(read_desc, desc)

    def test_compressed_files(self):
        cookie_desc = magic_open(MAGIC_COMPRESS)
        cookie_mime = magic_open(MAGIC_MIME_TYPE | MAGIC_COMPRESS)
        cookie_charset = magic_open(MAGIC_MIME_ENCODING | MAGIC_COMPRESS)
        cookie_mime_full = magic_open(MAGIC_MIME | MAGIC_COMPRESS)

        magic_load(cookie_desc)
        magic_load(cookie_mime)
        magic_load(cookie_charset)
        magic_load(cookie_mime_full)

        for filename in sorted(TEST_FILES_COMPRESSED.keys()):
            mime, charset, desc, mime_charset = TEST_FILES_COMPRESSED[filename]

            file_path = os.path.join(TEST_DATA_DIR, filename)

            read_desc = magic_file(cookie_desc, file_path)
            read_mime = magic_file(cookie_mime, file_path)
            read_charset = magic_file(cookie_charset, file_path)
            read_mime_full = magic_file(cookie_mime_full, file_path)

            self.assertMatches(read_mime, mime)
            self.assertMatches(read_mime_full, mime_charset)
            self.assertMatches(read_charset, charset)
            self.assertMatches(read_desc, desc)
