from ctypes.util import find_library
import ctypes
import glob
import os
import subprocess
import sys

def _lib_candidates():
    here = os.path.dirname(__file__)

    if sys.platform == 'darwin':

        paths = [
            here,
            os.path.abspath('.'),
            '/opt/local/lib',
            '/usr/local/lib',
            '/opt/homebrew/lib',
        ] + glob.glob('/usr/local/Cellar/libmagic/*/lib')

        for i in paths:
            yield os.path.join(i, 'libmagic.dylib')

    elif sys.platform in ('win32', 'cygwin'):

        prefixes = ['libmagic', 'magic1', 'magic-1', 'cygmagic-1', 'libmagic-1', 'msys-magic-1']

        for i in prefixes:
            # find_library searches in %PATH% but not the current directory,
            # so look for both
            yield os.path.join(here, '%s.dll' % i)
            yield os.path.join(os.path.abspath('.'), '%s.dll' % i)
            yield find_library(i)

    elif sys.platform == 'linux':

        prefixes = ['libmagic.so.1', 'libmagic.so']

        for i in prefixes:
            yield os.path.join(here, i)
            yield os.path.join(os.path.abspath('.'), i)
            # on some linux systems (musl/alpine), find_library('magic') returns None
            # first try ldconfig with backup string in case of error
            yield subprocess.check_output(
                "( ldconfig -p | grep '{0}' | grep -o '/.*' ) || echo '/usr/lib/{0}'".format(i),
                shell=True,
                universal_newlines=True,
            ).strip()

    yield find_library('magic')


def load_lib():

    for lib in _lib_candidates():
        # find_library returns None when lib not found
        if lib is None:
            continue
        try:
            return ctypes.CDLL(lib)
        except OSError:  # file not found
            pass
    raise ImportError('failed to find libmagic. Check your installation')

