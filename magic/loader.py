import ctypes
import glob
import logging
import os.path
import sys
from ctypes.util import find_library

logger = logging.getLogger(__name__)


def _lib_candidates_linux():
    """Yield possible libmagic library names on Linux.

    This is necessary because alpine is bad.

    Use `ldconfig -p | grep libmagic || true` to discover these.
    """
    yield from (
        "libmagic.so",
        "libmagic.so.1",
        "/lib/x86_64-linux-gnu/libmagic.so.1",
        "/lib/aarch64-linux-gnu/libmagic.so.1",
        "/lib/aarch64-linux-gnu/libmagic.so",
    )


def _lib_candidates_macos():
    """Yield possible libmagic library names on macOS."""
    paths = [
        "/opt/homebrew/lib",
        "/opt/local/lib",
        "/usr/local/lib",
    ] + glob.glob("/usr/local/Cellar/libmagic/*/lib")
    # Should probably use $HOMEBREW_CELLAR enviroment variable
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
        yield f"./{prefix}.dll"
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
    for lib in _lib_candidates():
        # find_library returns None when lib not found
        if lib is None:
            continue
        if not os.path.exists(lib):
            continue

        try:
            return ctypes.CDLL(lib)
        except OSError:
            logger.warning("Failed to load: " + lib, exc_info=True)

    # It is better to raise an ImportError since we are importing magic module
    raise ImportError("python-magic: failed to find libmagic.  Check your installation")
