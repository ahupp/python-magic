"""
This is the more Pythonic / nicer version..
"""

import os

from magic.wrapper import MAGIC_NONE, magic_open, magic_load, magic_buffer, \
    magic_file, magic_close, magic_setflags, MAGIC_MIME_TYPE, \
    MAGIC_MIME_ENCODING


## Internal use constants
FROM_FILE = 1
FROM_BUFFER = 2


class Magic(object):
    """
    Object-oriented version of the library..
    """

    _flags = None
    _cookie = None

    def __init__(self, flags=None, magic_db=None):
        self._flags = flags or MAGIC_NONE
        self._cookie = magic_open(self.flags)
        magic_load(self._cookie, magic_db)

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self.setflags(value)

    def setflags(self, flags):
        self._flags = flags
        magic_setflags(self._cookie, flags)

    def from_buffer(self, buf):
        return magic_buffer(self._cookie, buf)

    def from_file(self, filename):
        if not os.path.exists(filename):
            raise IOError("File does not exist: " + filename)
        return magic_file(self._cookie, filename)

    def close(self):
        magic_close(self._cookie)

    def __del__(self):
        ## during shutdown magic_close may have been cleared already
        if self._cookie and magic_close:
            self.close()
            self._cookie = None


class Magic2(object):
    """
    More natural, yet less efficient implementation of the library.
    """

    def __init__(self, from_type, from_arg, flags=None):
        self._from = from_type
        self._from_arg = from_arg
        self._cookie = None
        self._loaded = False
        self.flags = flags or MAGIC_NONE

    def _open(self, flags=MAGIC_NONE):
        self._cookie = magic_open(flags)

    def _close(self):
        magic_close(self._cookie)
        self._cookie = None

    def __del__(self):
        ## during shutdown magic_close may have been cleared already
        if self._cookie and magic_close:
            self._close()

    def _load(self, filename=None):
        magic_load(self._cookie, filename)
        self._loaded = True

    def _setflags(self, flags):
        magic_setflags(self._cookie, flags)

    def _prepare(self):
        if self._cookie is None:
            self._open()
        if not self._loaded:
            self._load()

    def _return(self):
        if self._from == FROM_FILE:
            return magic_file(self._cookie, self._from_arg)
        if self._from == FROM_BUFFER:
            return magic_buffer(self._cookie, self._from_arg)
        raise ValueError

    @classmethod
    def from_file(cls, filename, flags=None):
        return cls(from_type=FROM_FILE, from_arg=filename, flags=flags)

    @classmethod
    def from_buffer(cls, buf, flags=None):
        return cls(from_type=FROM_BUFFER, from_arg=buf, flags=flags)

    @property
    def description(self):
        self._prepare()
        self._setflags(
            self.flags
            & ~MAGIC_MIME_TYPE
            & ~MAGIC_MIME_ENCODING
        )
        return self._return()

    @property
    def mimetype(self):
        self._prepare()
        self._setflags(
            self.flags
            | MAGIC_MIME_TYPE
            & ~MAGIC_MIME_ENCODING
        )
        return self._return()

    @property
    def encoding(self):
        self._prepare()
        self._setflags(
            self.flags
            & ~MAGIC_MIME_TYPE
            | MAGIC_MIME_ENCODING
        )
        return self._return()

    @property
    def mime(self):
        self._prepare()
        self._setflags(
            self.flags
            | MAGIC_MIME_TYPE
            | MAGIC_MIME_ENCODING
        )
        return self._return()

    def __str__(self):
        return self.description

    def __unicode__(self):
        return unicode(self.description)
