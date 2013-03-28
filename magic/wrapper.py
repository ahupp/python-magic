"""
magic is a wrapper around the libmagic file identification library.
"""

import sys
import ctypes
import ctypes.util

from ctypes import c_char_p, c_int, c_size_t, c_void_p

__all__ = [
    "magic_open", "magic_close", "magic_error", "magic_errno",
    "magic_file", "magic_buffer", "magic_load", "magic_setflags",
    "magic_check", "magic_compile", "MAGIC_NONE", "MAGIC_DEBUG",
    "MAGIC_SYMLINK", "MAGIC_COMPRESS", "MAGIC_DEVICES", "MAGIC_MIME_TYPE",
    "MAGIC_MIME_ENCODING", "MAGIC_CONTINUE", "MAGIC_CHECK",
    "MAGIC_PRESERVE_ATIME", "MAGIC_RAW", "MAGIC_ERROR",
    "MAGIC_NO_CHECK_COMPRESS", "MAGIC_NO_CHECK_TAR", "MAGIC_NO_CHECK_SOFT",
    "MAGIC_NO_CHECK_APPTYPE", "MAGIC_NO_CHECK_ELF", "MAGIC_NO_CHECK_ASCII",
    "MAGIC_NO_CHECK_TROFF", "MAGIC_NO_CHECK_FORTRAN", "MAGIC_NO_CHECK_TOKENS",
    "MagicException",
]


class MagicException(Exception):
    pass


## Find and load the libmagic library

libmagic = None
# Let's try to find magic or magic1
dll = ctypes.util.find_library('magic') or ctypes.util.find_library('magic1')

## This is necessary because find_library returns None if it doesn't
## find the library
if dll:
    libmagic = ctypes.CDLL(dll)

if not libmagic or not libmagic._name:
    platform_to_lib = {
        'darwin': [
            '/opt/local/lib/libmagic.dylib',
            '/usr/local/lib/libmagic.dylib',
            '/usr/local/Cellar/libmagic/5.10/lib/libmagic.dylib'],
        'win32': ['magic1.dll'],
    }
    for dll in platform_to_lib.get(sys.platform, []):
        try:
            libmagic = ctypes.CDLL(dll)
        except OSError:
            pass

if not libmagic or not libmagic._name:
    # It is better to raise an ImportError since we are importing magic module
    raise ImportError('failed to find libmagic.  Check your installation')

magic_t = ctypes.c_void_p


def errorcheck(result, func, args):
    err = magic_error(args[0])
    if err is not None:
        raise MagicException(err)
    else:
        return result


def coerce_filename(filename):
    if filename is None:
        return None
    return filename.encode(sys.getfilesystemencoding())


magic_open = libmagic.magic_open
magic_open.restype = magic_t
magic_open.argtypes = [c_int]

magic_close = libmagic.magic_close
magic_close.restype = None
magic_close.argtypes = [magic_t]

magic_error = libmagic.magic_error
magic_error.restype = c_char_p
magic_error.argtypes = [magic_t]

magic_errno = libmagic.magic_errno
magic_errno.restype = c_int
magic_errno.argtypes = [magic_t]

_magic_file = libmagic.magic_file
_magic_file.restype = c_char_p
_magic_file.argtypes = [magic_t, c_char_p]
_magic_file.errcheck = errorcheck


def magic_file(cookie, filename):
    return _magic_file(cookie, coerce_filename(filename))


_magic_buffer = libmagic.magic_buffer
_magic_buffer.restype = c_char_p
_magic_buffer.argtypes = [magic_t, c_void_p, c_size_t]
_magic_buffer.errcheck = errorcheck


def magic_buffer(cookie, buf):
    return _magic_buffer(cookie, buf, len(buf))


_magic_load = libmagic.magic_load
_magic_load.restype = c_int
_magic_load.argtypes = [magic_t, c_char_p]
_magic_load.errcheck = errorcheck


def magic_load(cookie, filename):
    return _magic_load(cookie, coerce_filename(filename))


magic_setflags = libmagic.magic_setflags
magic_setflags.restype = c_int
magic_setflags.argtypes = [magic_t, c_int]

magic_check = libmagic.magic_check
magic_check.restype = c_int
magic_check.argtypes = [magic_t, c_char_p]

magic_compile = libmagic.magic_compile
magic_compile.restype = c_int
magic_compile.argtypes = [magic_t, c_char_p]


## Flags

MAGIC_NONE = 0x000000  # No flags
MAGIC_DEBUG = 0x000001  # Turn on debugging
MAGIC_SYMLINK = 0x000002  # Follow symlinks
MAGIC_COMPRESS = 0x000004  # Check inside compressed files
MAGIC_DEVICES = 0x000008  # Look at the contents of devices
MAGIC_MIME = MAGIC_MIME_TYPE = 0x000010  # Return a mime string
MAGIC_MIME_ENCODING = 0x000400  # Return the MIME encoding
MAGIC_CONTINUE = 0x000020  # Return all matches
MAGIC_CHECK = 0x000040  # Print warnings to stderr
MAGIC_PRESERVE_ATIME = 0x000080  # Restore access time on exit
MAGIC_RAW = 0x000100  # Don't translate unprintable chars
MAGIC_ERROR = 0x000200  # Handle ENOENT etc as real errors
MAGIC_NO_CHECK_COMPRESS = 0x001000  # Don't check for compressed files
MAGIC_NO_CHECK_TAR = 0x002000  # Don't check for tar files
MAGIC_NO_CHECK_SOFT = 0x004000  # Don't check magic entries
MAGIC_NO_CHECK_APPTYPE = 0x008000  # Don't check application type
MAGIC_NO_CHECK_ELF = 0x010000  # Don't check for elf details
MAGIC_NO_CHECK_ASCII = 0x020000  # Don't check for ascii files
MAGIC_NO_CHECK_TROFF = 0x040000  # Don't check ascii/troff
MAGIC_NO_CHECK_FORTRAN = 0x080000  # Don't check ascii/fortran
MAGIC_NO_CHECK_TOKENS = 0x100000  # Don't check ascii/tokens
