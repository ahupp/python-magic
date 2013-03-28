"""
Test data for the tests.
"""

import os
envvar = 'PYMAGIC_TEST_DATA'
if envvar in os.environ:
    TEST_DATA_DIR = os.environ[envvar]
else:
    TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


TEST_FILES = {
    "magic27.pyc_":       (
        b"application/octet-stream",
        b"binary",
        b"python 2.7 byte-compiled",
        b"application/octet-stream; charset=binary",
    ),
    "magic.pyc_":         (
        b"application/octet-stream",
        b"binary",
        b"python 2.4 byte-compiled",
        b"application/octet-stream; charset=binary",
    ),
    "test.gz":            (
        b"application/x-gzip",
        b"binary",
        b"gzip compressed data, was \"test\", from Unix, last modified: Sun Jun 29 03:32:52 2008",
        b"application/x-gzip; charset=binary",
    ),
    "test.pdf":           (
        b"application/pdf",
        b"us-ascii",
        b"PDF document, version 1.2",
        b"application/pdf; charset=us-ascii",
    ),
    "text-iso8859-1.txt": (
        b"text/plain",
        b"iso-8859-1",
        b"ISO-8859 text",
        b"text/plain; charset=iso-8859-1",
    ),
    "text.txt":           (
        b"text/plain",
        b"us-ascii",
        b"ASCII text",
        b"text/plain; charset=us-ascii",
    ),
}

TEST_FILES_COMPRESSED = {
    "magic27.pyc_":       (
        b"application/octet-stream",
        b"binary",
        b"python 2.7 byte-compiled",
        b"application/octet-stream; charset=binary",
    ),
    "magic.pyc_":         (
        b"application/octet-stream",
        b"binary",
        b"python 2.4 byte-compiled",
        b"application/octet-stream; charset=binary",
    ),
    "test.gz":            (
        b"text/plain",
        b"us-asciibinarybinary",
        b"ASCII text (gzip compressed data, was \"test\", from Unix, last modified: Sun Jun 29 03:32:52 2008)",
        b"text/plain; charset=us-ascii compressed-encoding=application/x-gzip; charset=binary; charset=binary",
    ),
    "test.pdf":           (
        b"application/pdf",
        b"us-ascii",
        b"PDF document, version 1.2",
        b"application/pdf; charset=us-ascii",
    ),
    "text-iso8859-1.txt": (
        b"text/plain",
        b"iso-8859-1",
        b"ISO-8859 text",
        b"text/plain; charset=iso-8859-1",
    ),
    "text.txt":           (
        b"text/plain",
        b"us-ascii",
        b"ASCII text",
        b"text/plain; charset=us-ascii",
    ),
}
