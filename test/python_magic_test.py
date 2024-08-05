import os
import os.path
import shutil
import sys
import tempfile

import pytest

# for output which reports a local time
os.environ["TZ"] = "GMT"

# this ensure we're in a utf-8 default filesystem encoding which is
# necessary for some tests
assert os.environ.get("LC_ALL", "") != "en_US.UTF-8", "must run `export LC_ALL=en_US.UTF-8` before running test suite"
assert sys.getfilesystemencoding().lower() == "utf-8"

import magic


TESTDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))


COMMON_PLAIN = [
    {},
    {"check_soft": True},
    {"check_soft": False},
    {"check_json": True},
    {"check_json": False},
]

NO_SOFT = [{"check_soft": False}]

COMMON_MIME = [{"mime": True, **k} for k in COMMON_PLAIN]

CASES_COMPACT = {
    "magic._pyc_": [
        (COMMON_MIME, [
            "application/octet-stream",
            "text/x-bytecode.python",
            "application/x-bytecode.python",
        ]),
        (COMMON_PLAIN, ["python 2.4 byte-compiled"]),
        (NO_SOFT, ["data"]),
    ],
    "test.pdf": [
        (COMMON_MIME, ["application/pdf"]),
        (COMMON_PLAIN, [
            "PDF document, version 1.2",
            "PDF document, version 1.2, 2 pages",
            "PDF document, version 1.2, 2 page(s)",
        ]),
        (NO_SOFT, ["ASCII text"]),
    ],
    "test.gz": [
        (COMMON_MIME, ["application/gzip", "application/x-gzip"]),
        (COMMON_PLAIN, [
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
        (COMMON_PLAIN, ["Apache Parquet", "Par archive data"]),
        (NO_SOFT, ["data"]),
    ],
    "test.json": [
        # TODO: soft, no_json
        (COMMON_MIME, ["application/json"]),
        (COMMON_PLAIN, ["JSON text data"]),
        ([{"mime": True, "check_json": False}], [
            "data",
        ]),
        (NO_SOFT, ["JSON text data"])
    ],
    "elf-NetBSD-x86_64-echo": [
        # TODO: soft, no elf
        (COMMON_PLAIN, [
            "ELF 64-bit LSB shared object, x86-64, version 1 (SYSV)",
            "ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /libexec/ld.elf_so, for NetBSD 8.0, not stripped",
        ]),
        (COMMON_MIME, [
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
    b"\xce\xbb": [
        (COMMON_MIME, ["text/plain"]),
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
            "image/jpeg"
        ]),
        ([{"mime": True, "keep_going": True}], [
            "image/jpeg\\012- application/octet-stream",
        ])
    ],
    "test.py": [
        (COMMON_MIME, [
            "text/x-python",
            "text/x-script.python",
        ])
    ]
}

def _unroll_cases():
    for file_base, cases in CASES_COMPACT.items():
        if type(file_base) is bytes:
            filename = os.path.join(TESTDATA_DIR.encode("utf-8"), file_base)
        else:
            filename = os.path.join(TESTDATA_DIR, file_base)
        for (all_flags, outputs) in cases:
            for flags in all_flags:
                yield filename, flags, outputs

TEST_CASES = list(_unroll_cases())

def test_version():
    try:
        assert magic.version() > 0
    except NotImplementedError:
        pass


def test_unicode_result_pgp():
    src = os.path.join(TESTDATA_DIR, "pgpunicode")
    for is_raw in [True, False]:
        m = magic.Magic(raw=is_raw)
        result = m.from_file(src)
        if "PGP" in result:
            assert b"PGP\tSecret Sub-key -" == result.encode("utf-8")
        else:
            pytest.skip("Magic file doesn't return expected type for PGP")


def test_errors():
    m = magic.Magic()
    with pytest.raises(IOError):
        m.from_file("nonexistent")
    with pytest.raises(magic.MagicException):
        magic.Magic(magic_file="nonexistent")

    os.environ["MAGIC"] = "nonexistent"
    try:
        with pytest.raises(magic.MagicException):
            magic.Magic()
    finally:
        del os.environ["MAGIC"]


def test_rethrow():
    old = magic.magic_buffer
    try:

        def t(x, y):
            raise magic.MagicException("passthrough")

        magic.magic_buffer = t

        with pytest.raises(magic.MagicException):
            magic.from_buffer("hello", True)
    finally:
        magic.magic_buffer = old

def test_getparam():
    m = magic.Magic(mime=True)
    try:
        m.setparam(magic.MAGIC_PARAM_INDIR_MAX, 1)
        assert m.getparam(magic.MAGIC_PARAM_INDIR_MAX) == 1
    except NotImplementedError:
        pass


def test_symlink():
    # TODO: 3.0
    if not hasattr(tempfile, "TemporaryDirectory"):
        return

    with tempfile.TemporaryDirectory() as tmp:
        tmp_link = os.path.join(tmp, "test_link")
        tmp_broken = os.path.join(tmp, "nonexistent")

        os.symlink(
            os.path.join(TESTDATA_DIR, "test.pdf"),
            tmp_link,
        )

        os.symlink("/nonexistent", tmp_broken)

        m = magic.Magic()
        m_follow = magic.Magic(follow_symlinks=True)
        assert m.from_file(tmp_link).startswith("symbolic link to ")
        assert m_follow.from_file(tmp_link).startswith("PDF document")

        assert m.from_file(tmp_broken).startswith(
                "broken symbolic link to /nonexistent"
            )

        with pytest.raises(IOError):
            m_follow.from_file(tmp_broken)


@pytest.mark.parametrize("file_name,flags,outputs", TEST_CASES)
def test_files(file_name, flags, outputs):

    # TODO:
    # * MAGIC_EXTENSION not supported
    dest = os.path.join(TESTDATA_DIR, b"\xce\xbb".decode("utf-8"))
    shutil.copyfile(os.path.join(TESTDATA_DIR, "lambda"), dest)
    os.environ["TZ"] = "UTC"
    try:
        m = magic.Magic(**flags)
        with open(file_name) as f:
            assert m.from_descriptor(f.fileno()) in outputs

        assert m.from_file(file_name) in outputs

        if sys.version_info >= (3, 6) and type(file_name) is not bytes:
            from pathlib import Path
            path = Path(file_name)
            assert m.from_file(path) in outputs

        with open(file_name, "rb") as f:
            buf_result = m.from_buffer(f.read(1024))
            assert buf_result in outputs
    finally:
        del os.environ["TZ"]
        os.unlink(dest)
