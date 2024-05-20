from __future__ import annotations

from pathlib import Path
from sys import version_info
from warnings import filterwarnings

import pytest

from magic import what

filterwarnings("ignore", message="'imghdr' is deprecated")
try:  # imghdr was removed from the standard library in Python 3.13
    from imghdr import what as imghdr_what
except ModuleNotFoundError:
    imghdr_what = None

# file_tests = sorted(test_func.__name__[5:] for test_func in imghdr.tests)
# file_tests = "bmp exr gif jpg pbm pgm png ppm ras rgb tif webp xbm".split()


@pytest.mark.skipif(imghdr_what is None, reason="imghdr was removed from the standard library in Python 3.13")
@pytest.mark.parametrize("file", [
    "keep-going.jpg",
    "name_use.jpg"
])
def test_what_from_file(file, h=None):
    """Run each test with a path string and a pathlib.Path."""
    # expected = file.split(".")[-1]
    # if expected == "jpeg":
    #     expected = "jpg"
    file = f"test/testdata/{file}"
    assert what(file, h) == imghdr_what(file, h)
    file = Path(file).resolve()
    assert what(file, h) == imghdr_what(file, h)


@pytest.mark.skipif(imghdr_what is None, reason="imghdr was removed from the standard library in Python 3.13")
def ztest_what_from_file_none(file="test/resources/fake_file", h=None):
    assert what(file, h) == imghdr_what(file, h) is None
    file = Path(file).resolve()
    assert what(file, h) == imghdr_what(file, h) is None


string_tests = [
    ("exr", "762f3101"),
    ("exr", b"\x76\x2f\x31\x01"),
    ("gif", "474946383761"),
    ("gif", b"GIF87a"),
    ("gif", b"GIF89a"),
    ("rast", b"\x59\xA6\x6A\x95"),
    ("rgb", b"\001\332"),
    ("webp", b"RIFF____WEBP"),
    (None, "decafbad"),
    (None, b"decafbad"),
]


@pytest.mark.skipif(imghdr_what is None, reason="imghdr was removed from the standard library in Python 3.13")
@pytest.mark.parametrize("expected, h", string_tests)
def test_what_from_string(expected, h):
    if isinstance(h, str):  # In imgdir.what() h must be bytes, not str.
        h = bytes.fromhex(h)
    assert imghdr_what(None, h) == what(None, h) == expected


@pytest.mark.skipif(imghdr_what is None, reason="imghdr was removed from the standard library in Python 3.13")
@pytest.mark.parametrize(
    "expected, h",
    [
        ("jpeg", "ffd8ffdb"),
        ("jpeg", b"\xff\xd8\xff\xdb"),
    ],
)
def test_what_from_string_py311(expected, h):
    """
    These tests fail with imghdr on Python < 3.11.
    TODO: (cclauss) Document these imghdr fails on Python < 3.11
    """
    if isinstance(h, str):  # In imgdir.what() h must be bytes, not str.
        h = bytes.fromhex(h)
    assert what(None, h) == expected
    if version_info < (3, 11):  # TODO: Document these imghdr fails
        expected = None
    assert imghdr_what(None, h) == expected


@pytest.mark.skipif(imghdr_what is None, reason="imghdr was removed from the standard library in Python 3.13")
@pytest.mark.parametrize(
    "expected, h",
    [
        ("bmp", "424d"),
        ("bmp", "424d787878785c3030305c303030"),
        ("bmp", b"BM"),
        ("jpeg", b"______JFIF"),
        ("jpeg", b"______Exif"),
        ("pbm", b"P1 "),
        ("pbm", b"P1\n"),
        ("pbm", b"P1\r"),
        ("pbm", b"P1\t"),
        ("pbm", b"P4 "),
        ("pbm", b"P4\n"),
        ("pbm", b"P4\r"),
        ("pbm", b"P4\t"),
        ("pgm", b"P2 "),
        ("pgm", b"P2\n"),
        ("pgm", b"P2\r"),
        ("pgm", b"P2\t"),
        ("pgm", b"P5 "),
        ("pgm", b"P5\n"),
        ("pgm", b"P5\r"),
        ("pgm", b"P5\t"),
        ("png", "89504e470d0a1a0a"),
        ("png", b"\211PNG\r\n\032\n"),
        ("ppm", b"P3 "),
        ("ppm", b"P3\n"),
        ("ppm", b"P3\r"),
        ("ppm", b"P3\t"),
        ("ppm", b"P6 "),
        ("ppm", b"P6\n"),
        ("ppm", b"P6\r"),
        ("ppm", b"P6\t"),
        ("tiff", b"II"),
        ("tiff", b"MM"),
        ("xbm", b"#define "),
    ],
)
def test_what_from_string_todo(expected, h):
    """
    These tests pass with imghdr but fail with magic.
    TODO: (cclauss) Fix these magic fails
    """
    if isinstance(h, str):  # In imgdir.what() h must be bytes, not str.
        h = bytes.fromhex(h)
    assert imghdr_what(None, h) == expected
    assert what(None, h) is None
