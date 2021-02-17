import ctypes
import sys
import glob

def load_lib():
  libmagic = None
  # Let's try to find magic or magic1
  dll = ctypes.util.find_library('magic') \
        or ctypes.util.find_library('magic1') \
        or ctypes.util.find_library('cygmagic-1') \
        or ctypes.util.find_library('libmagic-1') \
        or ctypes.util.find_library('msys-magic-1')  # for MSYS2

  # necessary because find_library returns None if it doesn't find the library
  if dll:
      libmagic = ctypes.CDLL(dll)

  if not libmagic or not libmagic._name:
      windows_dlls = ['magic1.dll', 'cygmagic-1.dll', 'libmagic-1.dll', 'msys-magic-1.dll']
      platform_to_lib = {'darwin': ['/opt/local/lib/libmagic.dylib',
                                    '/usr/local/lib/libmagic.dylib'] +
                                  # Assumes there will only be one version installed
                                  glob.glob('/usr/local/Cellar/libmagic/*/lib/libmagic.dylib'),  # flake8:noqa
                        'win32': windows_dlls,
                        'cygwin': windows_dlls,
                        'linux': ['libmagic.so.1'],
                        # fallback for some Linuxes (e.g. Alpine) where library search does not work # flake8:noqa
                        }
      platform = 'linux' if sys.platform.startswith('linux') else sys.platform
      for dll in platform_to_lib.get(platform, []):
          try:
              libmagic = ctypes.CDLL(dll)
              break
          except OSError:
              pass

  if not libmagic or not libmagic._name:
      # It is better to raise an ImportError since we are importing magic module
      raise ImportError('failed to find libmagic.  Check your installation')
  return libmagic