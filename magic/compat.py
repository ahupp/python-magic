"""
Compatibility functions
"""

from .pythonic import Magic2

__all__ = ['from_buffer', 'from_file']


def from_file(filename, mime=False):
    m = Magic2.from_file(filename)
    return m.mimetype if mime else m.description


def from_buffer(buf, mime=False):
    m = Magic2.from_buffer(buf)
    return m.mimetype if mime else m.description
