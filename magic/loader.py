from ctypes.util import find_library
import ctypes
import sys
import glob
import os
import logging
import subprocess

logger = logging.getLogger(__name__)
here = os.path.dirname(__file__)

def _lib_candidates_linux():
    """Yield possible libmagic library names on Linux."""
    fnames = ('libmagic.so.1', 'libmagic.so')

    for fname in fnames:
        # libmagic bundled in the wheel
        yield os.path.join(here, fname)
        # libmagic in the current working directory
        yield os.path.join(os.path.abspath('.'), fname)
        # libmagic install from source default destination path
        yield os.path.join('/usr/local/lib', fname)
        # on some linux systems (musl/alpine), find_library('magic') returns None
        # first try finding libmagic using ldconfig
        # otherwise fall back to /usr/lib/
        yield subprocess.check_output(
            "( ldconfig -p | grep '{0}' | grep -o '/.*' ) || echo '/usr/lib/{0}'".format(fname),
            shell=True,
            universal_newlines=True,
        ).strip()


def _lib_candidates_macos():
    """Yield possible libmagic library names on macOS."""
    paths = [
        # libmagic bundled in the wheel
        here,
        # libmagic in the current working directory
        os.path.abspath('.'),
        # libmagic in other common sources like homebrew
        '/opt/local/lib',
        '/usr/local/lib',
        '/opt/homebrew/lib',
    ] + glob.glob('/usr/local/Cellar/libmagic/*/lib')

    for path in paths:
        yield os.path.join(path, 'libmagic.dylib')


def _lib_candidates_windows():
    """Yield possible libmagic library names on Windows."""
    fnames = (
        "libmagic",
        "magic1",
        "magic-1",
        "cygmagic-1",
        "libmagic-1",
        "msys-magic-1",
    )

    for fname in fnames:
        # libmagic bundled in the wheel
        yield os.path.join(here, '%s.dll' % fname)
        # libmagic in the current working directory
        yield os.path.join(os.path.abspath('.'), '%s.dll' % fname)
        # find_library searches in %PATH% but not the current directory
        yield find_library(fname)


def _lib_candidates():
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

    # fallback
    yield find_library('magic')


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
    raise ImportError("python-magic: failed to find libmagic. Check your installation")
