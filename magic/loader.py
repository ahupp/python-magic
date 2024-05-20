from ctypes.util import find_library
import ctypes
import sys
import glob
import os.path
import logging

logger = logging.getLogger(__name__)

def _lib_candidates_linux():
    """Yield possible libmagic library names on Linux.

    This is necessary because alpine is bad
    """
    for path in ("libmagic.so", "libmagic.so.1"):
        yield find_library(path)


def _lib_candidates_macos():
    """Yield possible libmagic library names on macOS."""
    paths = [
        "/opt/homebrew/lib",
        "/opt/local/lib",
        "/usr/local/lib",
    ] + glob.glob("/usr/local/Cellar/libmagic/*/lib")
    for path in paths:
        yield os.path.join(path, "libmagic.dylib")


def _lib_candidates_windows():
    """Yield possible libmagic library names on Windows."""
    prefixes = (
        "libmagic",
        "magic1",
        "magic-1",
        "cygmagic-1",
        "libmagic-1",
        "msys-magic-1",
    )
    for prefix in prefixes:
        # find_library searches in %PATH% but not the current directory,
        # so look for both
        yield "./%s.dll" % (prefix,)
        yield find_library(prefix)


def _lib_candidates():
    yield find_library("magic")

    func = {
        "cygwin": _lib_candidates_windows,
        "darwin": _lib_candidates_macos,
        "linux": _lib_candidates_linux,
        "win32": _lib_candidates_windows,
        "sunos5": _lib_candidates_linux, 
    }.get(sys.platform)
    if func is None:
        raise ImportError("python-magic: Unsupported platform: " + sys.platform)
    # When we drop legacy Python, we can just `yield from func()`
    for path in func():
        yield path


def load_lib():
    lib_candidates = tuple(lib for lib in _lib_candidates() if lib)
    for lib in _lib_candidates():
        # find_library returns None when lib not found
        try:
            return ctypes.CDLL(lib)
        except OSError:
            pass

    # It is better to raise an ImportError since we are importing magic module
    fmt = "python-magic: failed to find libmagic in {}.  Check your installation"
    raise ImportError(fmt.format(", ".join(lib_candidates)))
