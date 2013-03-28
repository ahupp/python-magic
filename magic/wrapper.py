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


def _errorcheck(result, func, args):
    err = magic_error(args[0])
    if err is not None:
        raise MagicException(err)
    else:
        return result


def _coerce_filename(filename):
    if filename is None:
        return None
    return filename.encode(sys.getfilesystemencoding())


_magic_open = libmagic.magic_open
_magic_open.restype = magic_t
_magic_open.argtypes = [c_int]


def magic_open(flags=0):
    """
    Creates a magic cookie pointer and returns it.
    It returns NULL if there was an error allocating the magic cookie.

    The flags argument specifies how the other magic functions should behave:

    MAGIC_NONE
        No special handling.

    MAGIC_DEBUG
        Print debugging messages to stderr.

    MAGIC_SYMLINK
        If the file queried is a symlink, follow it.

    MAGIC_COMPRESS
        If the file is compressed, unpack it and look at the contents.

    MAGIC_DEVICES
        If the file is a block or character special device, then open
        the device and try to look in its contents.

    MAGIC_MIME_TYPE
        Return a MIME type string, instead of a textual description.

    MAGIC_MIME_ENCODING
        Return a MIME encoding, instead of a textual description.

    MAGIC_CONTINUE
        Return all matches, not just the first.

    MAGIC_CHECK
        Check the magic database for consistency and print warnings to stderr.

    MAGIC_PRESERVE_ATIME
        On systems that support utime(2) or utimes(2), attempt to preserve
        the access time of files analyzed.

    MAGIC_RAW
        Don't translate unprintable characters to a \ooo octal representation.

    MAGIC_ERROR
        Treat operating system errors while trying to open files and follow
        symlinks as real errors, instead of printing them in the magic buffer.

    MAGIC_NO_CHECK_APPTYPE
        Check for EMX application type (only on EMX).

    MAGIC_NO_CHECK_ASCII
        Check for various types of ascii files.

    MAGIC_NO_CHECK_COMPRESS
        Don't look for, or inside compressed files.

    MAGIC_NO_CHECK_ELF
        Don't print elf details.

    MAGIC_NO_CHECK_FORTRAN
        Don't look for fortran sequences inside ascii files.

    MAGIC_NO_CHECK_SOFT
        Don't consult magic files.

    MAGIC_NO_CHECK_TAR
        Don't examine tar files.

    MAGIC_NO_CHECK_TOKENS
        Don't look for known tokens inside ascii files.

    MAGIC_NO_CHECK_TROFF
        Don't look for troff sequences inside ascii files.
    """
    return _magic_open(flags)


_magic_close = libmagic.magic_close
_magic_close.restype = None
_magic_close.argtypes = [magic_t]


def magic_close(cookie):
    """
    Close the magic database and deallocate any resources used
    """
    return _magic_close(cookie)


_magic_error = libmagic.magic_error
_magic_error.restype = c_char_p
_magic_error.argtypes = [magic_t]


def magic_error(cookie):
    """
    Returns a textual explanation of the last error, or NULL
    if there was no error.
    """
    return _magic_error(cookie)


_magic_errno = libmagic.magic_errno
_magic_errno.restype = c_int
_magic_errno.argtypes = [magic_t]


def magic_errno(cookie):
    """
    Returns the last operating system error number (errno(2))
    that was encountered by a system call.
    """
    return _magic_errno(cookie)


_magic_file = libmagic.magic_file
_magic_file.restype = c_char_p
_magic_file.argtypes = [magic_t, c_char_p]
_magic_file.errcheck = _errorcheck


def magic_file(cookie, filename=None):
    """
    Returns a textual description of the contents of the filename
    argument.

    If the filename is None, then stdin is used.
    """
    return _magic_file(cookie, _coerce_filename(filename))


_magic_buffer = libmagic.magic_buffer
_magic_buffer.restype = c_char_p
_magic_buffer.argtypes = [magic_t, c_void_p, c_size_t]
_magic_buffer.errcheck = _errorcheck


def magic_buffer(cookie, buf):
    """
    Returns a textual description of the contents of the buffer
    argument with length bytes size.
    """
    return _magic_buffer(cookie, buf, len(buf))


_magic_load = libmagic.magic_load
_magic_load.restype = c_int
_magic_load.argtypes = [magic_t, c_char_p]
_magic_load.errcheck = _errorcheck


def magic_load(cookie, filename=None):
    """
    Must be used to load the the colon separated list of database
    files passed in as filename, or NULL for the default database file
    before any magic queries can performed.
    """
    return _magic_load(cookie, _coerce_filename(filename))


_magic_setflags = libmagic.magic_setflags
_magic_setflags.restype = c_int
_magic_setflags.argtypes = [magic_t, c_int]


def magic_setflags(cookie, flags):
    """
    Sets the flags described above. Note that using both MIME flags
    together can also return extra information on the charset.
    """
    return _magic_setflags(cookie, flags)


_magic_check = libmagic.magic_check
_magic_check.restype = c_int
_magic_check.argtypes = [magic_t, c_char_p]


def magic_check(cookie, filename=None):
    """
    Check the validity of entries in the colon separated database
    files passed in as filename, or NULL for the default database.
    It returns 0 on success and -1 on failure.
    """
    return _magic_check(cookie, _coerce_filename(filename))


_magic_compile = libmagic.magic_compile
_magic_compile.restype = c_int
_magic_compile.argtypes = [magic_t, c_char_p]


def magic_compile(cookie, filename=None):
    """
    Compile the the colon separated list of database files passed in
    as filename, or NULL for the default database.

    It returns 0 on success and -1 on failure. The compiled files created
    are named from the basename(1) of each file argument with ''.mgc''
    appended to it.
    """
    return _magic_compile(cookie, _coerce_filename(filename))


## Flags

MAGIC_NONE              = 0x000000  # No flags
MAGIC_DEBUG             = 0x000001  # Turn on debugging
MAGIC_SYMLINK           = 0x000002  # Follow symlinks
MAGIC_COMPRESS          = 0x000004  # Check inside compressed files
MAGIC_DEVICES           = 0x000008  # Look at the contents of devices
MAGIC_MIME_TYPE         = 0x000010  # Return the MIME type
MAGIC_CONTINUE          = 0x000020  # Return all matches
MAGIC_CHECK             = 0x000040  # Print warnings to stderr
MAGIC_PRESERVE_ATIME    = 0x000080  # Restore access time on exit
MAGIC_RAW               = 0x000100  # Don't translate unprintable chars
MAGIC_ERROR             = 0x000200  # Handle ENOENT etc as real errors
MAGIC_MIME_ENCODING     = 0x000400  # Return the MIME encoding
MAGIC_MIME              = (MAGIC_MIME_TYPE|MAGIC_MIME_ENCODING)
MAGIC_APPLE             = 0x000800  # Return the Apple creator and type
MAGIC_NO_CHECK_COMPRESS = 0x001000  # Don't check for compressed files
MAGIC_NO_CHECK_TAR      = 0x002000  # Don't check for tar files
MAGIC_NO_CHECK_SOFT     = 0x004000  # Don't check magic entries
MAGIC_NO_CHECK_APPTYPE  = 0x008000  # Don't check application type
MAGIC_NO_CHECK_ELF      = 0x010000  # Don't check for elf details

## In libmagic 5.11-2
MAGIC_NO_CHECK_TEXT     = 0x020000  # Don't check for text files
MAGIC_NO_CHECK_CDF      = 0x040000  # Don't check for cdf files
MAGIC_NO_CHECK_TOKENS   = 0x100000  # Don't check tokens
MAGIC_NO_CHECK_ENCODING = 0x200000  # Don't check text encodings

## In an older version of the library, things
## were named differently..
MAGIC_NO_CHECK_ASCII   = 0x020000  # Don't check for ascii files
MAGIC_NO_CHECK_TROFF   = 0x040000  # Don't check ascii/troff
MAGIC_NO_CHECK_FORTRAN = 0x080000  # Don't check ascii/fortran
MAGIC_NO_CHECK_TOKENS  = 0x100000  # Don't check ascii/tokens
