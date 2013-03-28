"""
Test cases for the wrapped C library.
"""

import os
import unittest
from magic.wrapper import MAGIC_MIME, \
    MAGIC_MIME_ENCODING, MAGIC_COMPRESS, MAGIC_MIME_TYPE
from magic.pythonic import Magic, Magic2
from ._test_data import TEST_DATA_DIR, TEST_FILES, TEST_FILES_COMPRESSED


class TestMagicPythonic(unittest.TestCase):
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

            self.assertEqual(mime_type, read_mime_type)
            self.assertEqual(mime_encoding, read_mime_encoding)
            self.assertEqual(mime, read_mime)
            self.assertEqual(desc, read_desc)

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

            self.assertEqual(mime_type, read_mime_type)
            self.assertEqual(mime_encoding, read_mime_encoding)
            self.assertEqual(mime, read_mime)
            self.assertEqual(desc, read_desc)


class TestMagic2(unittest.TestCase):
    def test_files(self):
        for filename, expected in sorted(TEST_FILES.items()):
            mime_type, mime_encoding, desc, mime = expected

            file_path = os.path.join(TEST_DATA_DIR, filename)
            m = Magic2.from_file(file_path)

            self.assertEqual(mime_type, m.mimetype)
            self.assertEqual(mime_encoding, m.encoding)
            self.assertEqual(mime, m.mime)
            self.assertEqual(desc, m.description)

    def test_compressed_files(self):
        for filename, expected in sorted(TEST_FILES_COMPRESSED.items()):
            mime_type, mime_encoding, desc, mime = expected

            file_path = os.path.join(TEST_DATA_DIR, filename)
            m = Magic2.from_file(file_path, MAGIC_COMPRESS)

            self.assertEqual(mime_type, m.mimetype)
            self.assertEqual(mime_encoding, m.encoding)
            self.assertEqual(mime, m.mime)
            self.assertEqual(desc, m.description)
