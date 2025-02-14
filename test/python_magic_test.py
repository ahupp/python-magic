from dataclasses import dataclass
from enum import Enum
import os
import os.path
import shutil
import sys
import tempfile
import unittest
from typing import List, Optional

# for output which reports a local time
os.environ["TZ"] = "GMT"

if os.environ.get("LC_ALL", "") != "en_US.UTF-8":
    # this ensure we're in a utf-8 default filesystem encoding which is
    # necessary for some tests
    raise Exception("must run `export LC_ALL=en_US.UTF-8` before running test suite")

import magic

@dataclass
class TestFile:
    file_name: str
    mime_results: List[str]
    text_results: List[str]
    no_check_elf_results: Optional[List[str]]
    buf_equals_file: bool = True

# magic_descriptor is broken (?) in centos 7, so don't run those tests
SKIP_FROM_DESCRIPTOR = bool(os.environ.get("SKIP_FROM_DESCRIPTOR"))


COMMON_PLAIN = [
    {},
    {"check_soft": True},
    {"check_soft": False},
    {"check_json": True},
    {"check_json": False},
]

NO_SOFT = [{"check_soft": False}]

COMMON_MIME = [{"mime": True, **k} for k in COMMON_PLAIN]

CASES = {
    "magic._pyc_": [
        (COMMON_MIME, [
            "application/octet-stream",
            "text/x-bytecode.python",
            "application/x-bytecode.python",
        ]),
        (COMMON_PLAIN, ["python 2.4 byte-compiled", "data"]),
        (NO_SOFT, ["python 2.4 byte-compiled", "data"]),
    ],
    "test.pdf": [
        (COMMON_MIME, ["text/plain", "application/pdf"]),
        (COMMON_PLAIN, [
            "ASCII text",
            "PDF document, version 1.2",
            "PDF document, version 1.2, 2 pages",
            "PDF document, version 1.2, 2 page(s)",
        ]),
        (NO_SOFT, ["ASCII text"]),
    ],
    "test.gz": [
        (COMMON_MIME, ["application/octet-stream", "application/gzip", "application/x-gzip"]),
        (COMMON_PLAIN, [
            "data",
            'gzip compressed data, was "test", from Unix, last modified: Sun Jun 29 01:32:52 2008',
            'gzip compressed data, was "test", last modified: Sun Jun 29 01:32:52 2008, from Unix',
            'gzip compressed data, was "test", last modified: Sun Jun 29 01:32:52 2008, from Unix, original size 15',
            'gzip compressed data, was "test", last modified: Sun Jun 29 01:32:52 2008, from Unix, original size modulo 2^32 15',
            'gzip compressed data, was "test", last modified: Sun Jun 29 01:32:52 2008, from Unix, truncated',
        ]),
        ([{"extension": True}], [
            # some versions return '' for the extensions of a gz file,
            # including w/ the command line.  Who knows...
            "gz/tgz/tpz/zabw/svgz/adz/kmy/xcfgz",
            "gz/tgz/tpz/zabw/svgz",
            "",
            "???",
        ]),
        (NO_SOFT, ["data"]),
    ],
    "test.snappy.parquet": [
        (COMMON_MIME, ["application/octet-stream"]),
        (COMMON_PLAIN, ["data", "Apache Parquet", "Par archive data"]),
        (NO_SOFT, ["data"]),
    ],
    "test.json": [
        # TODO: soft, no_json
        (COMMON_MIME, ["text/plain", "application/json"]),
        (COMMON_PLAIN, ["ASCII text", "JSON text data"]),
        ([{"mime": True, "check_json": False}], [
            "text/plain", "data",
        ]),
        (NO_SOFT, ["JSON text data"])
    ],
    "elf-NetBSD-x86_64-echo": [
        # TODO: soft, no elf
        (COMMON_PLAIN, [
            "data",
            "ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)",
            "ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /libexec/ld.elf_so, for NetBSD 8.0, not stripped",
        ]),
        (COMMON_MIME, [
            "application/octet-stream",
            "application/x-pie-executable",
            "application/x-sharedlib",
        ]),
        ([{"check_elf": False}], [
            "ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)",
        ]),
        # TODO: sometimes
        #  "ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /libexec/ld.elf_so, for NetBSD 8.0, not stripped",

        (NO_SOFT, ["data"]),
    ],
    "text.txt": [
        (COMMON_MIME, ["text/plain"]),
        (COMMON_PLAIN, ["ASCII text"]),
        ([{"mime_encoding": True}], [
            "us-ascii",
        ]),
        (NO_SOFT, ["ASCII text"]),
    ],
    "text-iso8859-1.txt": [
        ([{"mime_encoding": True}], [
            "iso-8859-1",
        ]),
    ],
    b"\xce\xbb".decode("utf-8"): [
        (COMMON_MIME, ["text/plain"]),
    ],
    "name_use.jpg": [
        ([{"extension": True}], [
            "jpeg/jpg/jpe/jfif"
        ]),
    ],
    "keep-going.jpg": [
        (COMMON_MIME, [
            "application/octet-stream",
            "image/jpeg",
        ]),
        ([{"mime": True, "keep_going": True}], [
            "image/jpeg\\012- application/octet-stream",
        ])
    ],
    # "test.py": [
    #     (COMMON_MIME, [
    #         "text/x-python",
    #         "text/x-script.python",
    #     ])
    # ]
}

class MagicTest(unittest.TestCase):
    TESTDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))

    def test_version(self):
        try:
            self.assertTrue(magic.version() > 0)
        except NotImplementedError:
            pass

    def test_fs_encoding(self):
        self.assertEqual("utf-8", sys.getfilesystemencoding().lower())


    def test_from_file_str_and_bytes(self):
        filename = os.path.join(self.TESTDATA_DIR, "test.pdf")

        self.assertEqual("application/pdf", magic.from_file(filename, mime=True))
        self.assertEqual(
            "application/pdf", magic.from_file(filename.encode("utf-8"), mime=True)
        )


    def test_all_cases(self):
        # TODO:
        # * MAGIC_EXTENSION not supported
        # * keep_going not supported
        # * buffer checks
        dest = os.path.join(MagicTest.TESTDATA_DIR, b"\xce\xbb".decode("utf-8"))
        shutil.copyfile(os.path.join(MagicTest.TESTDATA_DIR, "lambda"), dest)
        os.environ["TZ"] = "UTC"
        try:
            for file_name, cases in CASES.items():
                filename = os.path.join(self.TESTDATA_DIR, file_name)
                for flags_list, outputs in cases:
                    for flags in flags_list:
                        m = magic.Magic(**flags)
                        with open(filename) as f:
                            self.assertIn(m.from_descriptor(f.fileno()), outputs)

                        self.assertIn(m.from_file(filename), outputs)

                        fname_bytes = filename.encode("utf-8")
                        self.assertIn(m.from_file(fname_bytes), outputs)

                        with open(filename, "rb") as f:
                            buf_result = m.from_buffer(f.read(1024))
                            self.assertIn(buf_result, outputs)
        finally:
            del os.environ["TZ"]
            os.unlink(dest)

    def test_unicode_result_nonraw(self):
        m = magic.Magic(raw=False)
        src = os.path.join(MagicTest.TESTDATA_DIR, "pgpunicode")
        result = m.from_file(src)
        # NOTE: This check is added as otherwise some magic files don't identify the test case as a PGP key.
        if "PGP" in result:
            assert r"PGP\011Secret Sub-key -" == result
        else:
            raise unittest.SkipTest("Magic file doesn't return expected type.")

    def test_unicode_result_raw(self):
        m = magic.Magic(raw=True)
        src = os.path.join(MagicTest.TESTDATA_DIR, "pgpunicode")
        result = m.from_file(src)
        if "PGP" in result:
            assert b"PGP\tSecret Sub-key -" == result.encode("utf-8")
        else:
            raise unittest.SkipTest("Magic file doesn't return expected type.")


    def test_errors(self):
        m = magic.Magic()
        self.assertRaises(IOError, m.from_file, "nonexistent")
        self.assertRaises(magic.MagicException, magic.Magic, magic_file="nonexistent")
        os.environ["MAGIC"] = "nonexistent"
        try:
            self.assertRaises(magic.MagicException, magic.Magic)
        finally:
            del os.environ["MAGIC"]


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
        with open(os.path.join(self.TESTDATA_DIR, "name_use.jpg"), "rb") as f:
            m.from_buffer(f.read())

    def test_pathlike(self):
        if sys.version_info < (3, 6):
            return
        from pathlib import Path

        path = Path(self.TESTDATA_DIR, "test.pdf")
        m = magic.Magic(mime=True)
        self.assertEqual("application/pdf", m.from_file(path))

    def test_symlink(self):
        # TODO: 3.0
        if not hasattr(tempfile, "TemporaryDirectory"):
            return

        with tempfile.TemporaryDirectory() as tmp:
            tmp_link = os.path.join(tmp, "test_link")
            tmp_broken = os.path.join(tmp, "nonexistent")

            os.symlink(
                os.path.join(self.TESTDATA_DIR, "test.pdf"),
                tmp_link,
            )

            os.symlink("/nonexistent", tmp_broken)

            m = magic.Magic()
            m_follow = magic.Magic(follow_symlinks=True)
            self.assertTrue(m.from_file(tmp_link).startswith("symbolic link to "))
            self.assertTrue(m_follow.from_file(tmp_link).startswith("PDF document"))

            self.assertTrue(
                m.from_file(tmp_broken).startswith(
                    "broken symbolic link to /nonexistent"
                )
            )

            self.assertRaises(IOError, m_follow.from_file, tmp_broken)


if __name__ == "__main__":
    unittest.main()
