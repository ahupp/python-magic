"""
Test cases for the wrapped C library.
"""

import os
import unittest
from magic.wrapper import MAGIC_MIME, \
    MAGIC_MIME_ENCODING, MAGIC_COMPRESS, MAGIC_MIME_TYPE
from magic.pythonic import Magic, Magic2
from ._test_data import TEST_DATA_DIR, TEST_FILES, TEST_FILES_COMPRESSED, MagicTestCaseMixin


class TestMagicPythonic(MagicTestCaseMixin, unittest.TestCase):
    def test_files(self):
        m_desc = Magic()
        m_mime_type = Magic(MAGIC_MIME_TYPE)
        m_mime_encoding = Magic(MAGIC_MIME_ENCODING)
        m_mime = Magic(MAGIC_MIME)

        for filename, expected in sorted(TEST_FILES.items()):
            mime_type, mime_encoding, desc, mime = expected

            file_path = os.path.join(TEST_DATA_DIR, filename)

            read_mime_type = m_mime_type.from_file(file_path)
            read_mime_encoding = m_mime_encoding.from_file(file_path)
            read_desc = m_desc.from_file(file_path)
            read_mime = m_mime.from_file(file_path)

            self.assertMatches(read_mime_type, mime_type)
            self.assertMatches(read_mime_encoding, mime_encoding)
            self.assertMatches(read_mime, mime)
            self.assertMatches(read_desc, desc)

    def test_compressed_files(self):
        m_desc = Magic(MAGIC_COMPRESS)
        m_mime_type = Magic(MAGIC_MIME_TYPE | MAGIC_COMPRESS)
        m_mime_encoding = Magic(MAGIC_MIME_ENCODING | MAGIC_COMPRESS)
        m_mime = Magic(MAGIC_MIME | MAGIC_COMPRESS)

        for filename, expected in sorted(TEST_FILES_COMPRESSED.items()):
            mime_type, mime_encoding, desc, mime = expected

            file_path = os.path.join(TEST_DATA_DIR, filename)

            read_mime_type = m_mime_type.from_file(file_path)
            read_mime_encoding = m_mime_encoding.from_file(file_path)
            read_desc = m_desc.from_file(file_path)
            read_mime = m_mime.from_file(file_path)

            self.assertMatches(read_mime_type, mime_type)
            self.assertMatches(read_mime_encoding, mime_encoding)
            self.assertMatches(read_mime, mime)
            self.assertMatches(read_desc, desc)


class TestMagic2(MagicTestCaseMixin, unittest.TestCase):
    def test_files(self):
        for filename, expected in sorted(TEST_FILES.items()):
            mime_type, mime_encoding, desc, mime = expected

            file_path = os.path.join(TEST_DATA_DIR, filename)
            m = Magic2.from_file(file_path)

            self.assertMatches(m.mimetype, mime_type)
            self.assertMatches(m.encoding, mime_encoding)
            self.assertMatches(m.mime, mime)
            self.assertMatches(m.description, desc)

    def test_compressed_files(self):
        for filename, expected in sorted(TEST_FILES_COMPRESSED.items()):
            mime_type, mime_encoding, desc, mime = expected

            file_path = os.path.join(TEST_DATA_DIR, filename)
            m = Magic2.from_file(file_path, MAGIC_COMPRESS)

            self.assertMatches(m.mimetype, mime_type)
            self.assertMatches(m.encoding, mime_encoding)
            self.assertMatches(m.mime, mime)
            self.assertMatches(m.description, desc)
