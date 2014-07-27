"""
magic is a wrapper around the libmagic file identification library.

See README for more information.

Usage:

>>> import magic
>>> magic.from_file("testdata/test.pdf")
'PDF document, version 1.2'
>>> magic.from_file("testdata/test.pdf", mime=True)
'application/pdf'
>>> magic.from_buffer(open("testdata/test.pdf").read(1024))
'PDF document, version 1.2'
>>>


"""

import sys
import glob
import os.path
import ctypes
import ctypes.util
import threading

from ctypes import c_char_p, c_int, c_size_t, c_void_p

class MagicException(Exception): pass

class Magic:
    """
    Magic is a wrapper around the libmagic C library.

    """

    def __init__(self, mime=False, magic_file=None, mime_encoding=False,
                 keep_going=False):
        """
        Create a new libmagic wrapper.

        mime - if True, mimetypes are returned instead of textual descriptions
        mime_encoding - if True, codec is returned
        magic_file - use a mime database other than the system default
        keep_going - don't stop at the first match, keep going
        """
        self.flags = MAGIC_NONE
        if mime:
            self.flags |= MAGIC_MIME
        elif mime_encoding:
            self.flags |= MAGIC_MIME_ENCODING
        if keep_going:
            self.flags |= MAGIC_CONTINUE

        self.cookie = magic_open(self.flags)

        magic_load(self.cookie, magic_file)

        self.thread = threading.currentThread()

        #Default mime-types for libmagic in an easy to access dictionary
        self.file_types = {'audio/x-dec-basic': ['audio'],
            'audio/mp4': ['animation'],
            'application/vnd.oasis.opendocument.chart-template': ['archive'],
            'image/x-polar-monitor-bitmap': ['images'],
            'application/x-ichitaro6': ['wordprocessors'],
            'video/quicktime': ['animation'],
            'application/vnd.oasis.opendocument.graphics': ['archive'],
            'application/dicom': ['images'],
            'application/x-gnumeric': ['gnumeric'],
            'application/x-java-applet': ['cafebabe'],
            'text/texmacs': ['lisp'],
            'application/mac-binhex40': ['macintosh'],
            'application/x-msaccess': ['database'],
            'text/x-texinfo': ['tex'],
            'application/x-java-pack200': ['cafebabe'],
            'application/x-dbf': ['database'],
            'application/x-123': ['msdos'],
            'text/x-perl': ['perl'],
            'text/x-python': ['python'],
            'application/x-epoc-opl': ['epoc'],
            'image/x-portable-greymap': ['images'],
            'image/gif': ['images'],
            'application/xml-sitemap': ['sgml'],
            'application/x-stuffit': ['macintosh'],
            'application/x-kdelnk': ['kde'],
            'text/x-makefile': ['make'],
            'text/x-asm': ['assembler'],
            'application/x-scribus': ['wordprocessors'],
            'application/x-font-ttf': ['fonts'],
            'video/3gpp': ['animation'],
            'image/x-coreldraw': ['riff'],
            'audio/x-aiff': ['iff'],
            'image/x-award-bmp': ['images'],
            'video/webm': ['matroska'],
            'image/x-paintnet': ['images'],
            'image/x-unknown': ['images'],
            'image/jpx': ['jpeg'],
            'video/mp4': ['animation'],
            'application/vnd.oasis.opendocument.image': ['archive'],
            'text/x-c++': ['c-lang'],
            'application/x-ichitaro4': ['wordprocessors'],
            'application/x-lha': ['archive', 'msdos'],
            'text/x-lua': ['tcl', 'lua'],
            'application/pgp-signature': ['pgp'],
            'application/xml': ['sgml'],
            'text/x-vcard': ['misctools'],
            'text/x-fortran': ['fortran'],
            'application/x-bittorrent': ['archive'],
            'model/vrml': ['animation'],
            'application/x-cpio': ['archive'],
            'audio/x-musepack': ['audio'],
            'application/x-quicktime-player': ['animation'],
            'application/x-freemind': ['wordprocessors'],
            'application/x-epoc-data': ['epoc'],
            'application/vnd.oasis.opendocument.text-web': ['archive'],
            'audio/x-unknown': ['audio'],
            'application/x-tokyocabinet-btree': ['database'],
            'audio/x-adpcm': ['audio'],
            'audio/midi': ['audio'],
            'application/pdf': ['pdf'],
            'application/vnd.oasis.opendocument.text': ['archive'],
            'application/pgp': ['pgp'],
            'image/x-xcursor': ['xwindows'],
            'image/x-xcf': ['gimp'],
            'application/vnd.oasis.opendocument.database': ['archive'],
            'image/jp2': ['animation', 'jpeg'],
            'application/x-font-sfn': ['fonts'],
            'image/svg+xml': ['sgml'],
            'application/jar': ['archive'],
            'image/x-canon-cr2': ['images'],
            'text/PGP': ['pgp', 'gnu'],
            'application/x-bzip2': ['compress'],
            'application/x-iso9660-image': ['filesystems'],
            'application/x-epoc-jotter': ['epoc'],
            'image/x-icon': ['msdos'],
            'audio/basic': ['audio'],
            'chemical/x-pdb': ['scientific'],
            'application/x-dvi': ['tex'],
            'image/x-portable-bitmap': ['images'],
            'application/x-mif': ['frame'],
            'video/x-sgi-movie': ['animation'],
            'audio/x-pn-realaudio': ['audio'],
            'application/postscript': ['printer'],
            'application/vnd.oasis.opendocument.text-master': ['archive'],
            'model/x3d': ['animation'],
            'video/x-ms-asf': ['animation'],
            'text/x-c': ['c-lang'],
            'application/x-executable': ['elf'],
            'video/x-matroska': ['matroska'],
            'application/x-rpm': ['rpm'],
            'application/vnd.oasis.opendocument.image-template': ['archive'],
            'application/x-gnupg-keyring': ['gnu'],
            'application/x-compress': ['compress'],
            'image/x-quicktime': ['animation'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['msooxml'],
            'application/x-elc': ['lisp'],
            'application/x-epoc-app': ['epoc'],
            'application/vnd.oasis.opendocument.presentation-template': ['archive'],
            'image/x-pcx': ['images'],
            'application/x-epoc-word': ['epoc'],
            'application/vnd.font-fontforge-sfd': ['fonts'],
            'audio/x-w64': ['riff'],
            'application/x-dosexec': ['msdos'],
            'application/x-sc': ['sc'],
            'text/html': ['sgml'],
            'image/x-epoc-sketch': ['epoc'],
            'application/x-tokyocabinet-fixed': ['database'],
            'application/x-coredump': ['elf'],
            'video/3gpp2': ['animation'],
            'application/x-eet': ['archive'],
            'application/x-xz': ['compress'],
            'application/x-arc': ['archive'],
            'text/rtf': ['rtf'],
            'image/png': ['images'],
            'video/mp2t': ['animation'],
            'image/x-dpx': ['images'],
            'application/zip': ['archive', 'msdos'],
            'application/x-tokyocabinet-hash': ['database'],
            'video/x-flv': ['flash'],
            'text/x-pascal': ['pascal'],
            'application/x-epoc-opo': ['epoc'],
            'application/x-epoc-agenda': ['epoc'],
            'application/vnd.oasis.opendocument.chart': ['archive'],
            'audio/x-flac': ['audio'],
            'application/x-epoc-sheet': ['epoc'],
            'audio/vnd.dolby.dd-raw': ['dolby'],
            'application/octet-stream': ['archive', 'elf', 'compress'],
            'image/x-lss16': ['linux'],
            'application/x-lrzip': ['compress'],
            'application/x-object': ['elf'],
            'application/x-quark-xpress-3': ['wordprocessors'],
            'text/x-po': ['gnu'],
            'rinex/broadcast': ['rinex'],
            'image/x-award-bioslogo': ['images'],
            'message/rfc822': ['mail.news'],
            'application/vnd.ms-cab-compressed': ['msdos'],
            'video/x-flc': ['animation'],
            'text/x-bcpl': ['c-lang'],
            'video/mpeg4-generic': ['animation'],
            'application/x-zoo': ['archive'],
            'text/x-m4': ['m4'],
            'application/vnd.oasis.opendocument.spreadsheet-template': ['archive'],
            'text/x-ruby': ['ruby'],
            'application/x-7z-compressed': ['compress'],
            'application/x-pgp-keyring': ['pgp'],
            'application/ogg': ['vorbis'],
            'text/x-tcl': ['tcl'],
            'text/x-tex': ['tex'],
            'text/x-shellscript': ['commands'],
            'audio/x-hx-aac-adts': ['animation'],
            'image/x-ms-bmp': ['images'],
            'image/x-x3f': ['images'],
            'image/jpm': ['jpeg'],
            'application/x-setupscript': ['windows'],
            'application/vnd.iccprofile': ['icc'],
            'text/x-gawk': ['commands'],
            'image/x-niff': ['images'],
            'application/vnd.oasis.opendocument.formula-template': ['archive'],
            'application/vnd.ms-fontobject': ['fonts'],
            'audio/x-ape': ['audio'],
            'application/x-ichitaro5': ['wordprocessors'],
            'application/vnd.oasis.opendocument.text-template': ['archive'],
            'application/vnd.oasis.opendocument.spreadsheet': ['archive'],
            'application/vnd.lotus-wordpro': ['msdos'],
            'application/vnd.oasis.opendocument.formula': ['archive'],
            'application/vnd.google-earth.kml+xml': ['kml'],
            'image/jpeg': ['jpeg'],
            'rinex/navigation': ['rinex'],
            'application/x-debian-package': ['archive'],
            'text/x-info': ['tex'],
            'text/x-nawk': ['commands'],
            'text/troff': ['troff'],
            'text/x-java': ['java'],
            'application/epub+zip': ['archive'],
            'message/news': ['mail.news'],
            'application/x-java-jce-keystore': ['java'],
            'application/marc': ['marc21'],
            'text/x-msdos-batch': ['msdos'],
            'image/tiff': ['images'],
            'video/mpv': ['animation'],
            'application/x-svr4-package': ['pkgadd'],
            'application/vnd.oasis.opendocument.graphics-template': ['archive'],
            'video/x-mng': ['animation'],
            'text/calendar': ['misctools'],
            'application/gzip': ['compress'],
            'text/x-diff': ['diff'],
            'application/vnd.ms-tnef': ['mail.news', 'msdos'],
            'application/vnd.ms-opentype': ['fonts'],
            'application/x-archive': ['archive'],
            'application/vnd.ms-excel': ['msdos'],
            'application/x-tex-tfm': ['tex'],
            'text/x-awk': ['commands'],
            'application/x-lharc': ['archive'],
            'audio/x-hx-aac-adif': ['animation'],
            'image/x-canon-crw': ['images'],
            'application/x-arj': ['archive'],
            'application/vnd.google-earth.kmz': ['kml'],
            'application/x-java-keystore': ['java'],
            'application/vnd.rn-realmedia': ['audio'],
            'image/x-epoc-mbm': ['epoc'],
            'rinex/observation': ['rinex'],
            'application/x-sharedlib': ['elf'],
            'image/x-exr': ['images'],
            'x-epoc/x-sisx-app': ['archive'],
            'application/x-ima': ['filesystems'],
            'application/x-ia-arc': ['warc'],
            'application/msword': ['msdos'],
            'application/x-gnucash': ['sgml'],
            'application/x-lzip': ['compress'],
            'image/x-cpi': ['images'],
            'application/x-rar': ['archive'],
            'application/pgp-keys': ['pgp'],
            'video/x-fli': ['animation'],
            'application/x-tar': ['archive'],
            'video/x-msvideo': ['riff'],
            'image/vnd.adobe.photoshop': ['images'],
            'image/x-portable-pixmap': ['images'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['msooxml'],
            'application/x-hdf': ['images'],
            'image/x-xpmi': ['images'],
            'application/vnd.cups-raster': ['cups'],
            'video/h264': ['animation'],
            'application/x-shockwave-flash': ['flash'],
            'audio/x-mp4a-latm': ['animation'],
            'image/x-xwindowdump': ['images'],
            'audio/x-wav': ['riff'],
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['msooxml'],
            'application/x-gdbm': ['database'],
            'application/vnd.tcpdump.pcap': ['sniffer'],
            'image/vnd.djvu': ['images'],
            'video/mp2p': ['animation'],
            'text/x-lisp': ['lisp'],
            'audio/mpeg': ['animation'],
            'application/x-tokyocabinet-table': ['database'],
            'audio/x-mod': ['audio'],
            'image/x-olympus-orf': ['images'],
            'application/vnd.symbian.install': ['archive'],
            'video/mpeg': ['animation'],
            'application/x-ms-reader': ['msdos'],
            'application/x-dbm': ['database'],
            'video/mj2': ['jpeg'],
            'text/x-xmcd': ['kde'],
            'application/x-hwp': ['wordprocessors'],
            'application/javascript': ['javascript'],
            'rinex/meteorological': ['rinex'],
            'rinex/clock': ['rinex'],
            'video/mp4v-es': ['animation'],
            'application/vnd.oasis.opendocument.presentation': ['archive'],
            'application/x-lzma': ['compress'],
            'text/x-php': ['commands'],
            'video/x-jng': ['animation']}

    def from_buffer(self, buf):
        """
        Identify the contents of `buf`
        """
        self._thread_check()
        try:
            return magic_buffer(self.cookie, buf)
        except MagicException as e:
            return self._handle509Bug(e)

    def from_file(self, filename):
        """
        Identify the contents of file `filename`
        raises IOError if the file does not exist
        """
        self._thread_check()
        if not os.path.exists(filename):
            raise IOError("File does not exist: " + filename)
        try:
            return magic_file(self.cookie, filename)
        except MagicException as e:
            return self._handle509Bug(e)

    def _handle509Bug(self, e):
        # libmagic 5.09 has a bug where it might mail to identify the
        # mimetype of a file and returns null from magic_file (and
        # likely _buffer), but also does not return an error message.
        if e.message is None and (self.flags & MAGIC_MIME):
            return "application/octet-stream"

    def _thread_check(self):
        if self.thread != threading.currentThread():
            raise Exception('attempting to use libmagic on multiple threads will '
                            'end in SEGV.  Prefer to use the module functions '
                            'from_file or from_buffer, or carefully manage direct '
                            'use of the Magic class')

    def __del__(self):
        # no _thread_check here because there can be no other
        # references to this object at this point.

        # during shutdown magic_close may have been cleared already so
        # make sure it exists before using it.

        # the self.cookie check should be unnessary and was an
        # incorrect fix for a threading problem, however I'm leaving
        # it in because it's harmless and I'm slightly afraid to
        # remove it.
        if self.cookie and magic_close:
            magic_close(self.cookie)
            self.cookie = None


instances = threading.local()

def _get_magic_type(mime):
    i = instances.__dict__.get(mime)
    if i is None:
        i = instances.__dict__[mime] = Magic(mime=mime)
    return i

def from_file(filename, mime=False):
    """"
    Accepts a filename and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_file("testdata/test.pdf", mime=True)
    'application/pdf'
    """
    m = _get_magic_type(mime)
    return m.from_file(filename)

def from_buffer(buffer, mime=False):
    """
    Accepts a binary string and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'
    """
    m = _get_magic_type(mime)
    return m.from_buffer(buffer)




libmagic = None
# Let's try to find magic or magic1
dll = ctypes.util.find_library('magic') or ctypes.util.find_library('magic1') or ctypes.util.find_library('cygmagic-1')

# This is necessary because find_library returns None if it doesn't find the library
if dll:
    libmagic = ctypes.CDLL(dll)

if not libmagic or not libmagic._name:
    platform_to_lib = {'darwin': ['/opt/local/lib/libmagic.dylib',
                                  '/usr/local/lib/libmagic.dylib'] +
                         # Assumes there will only be one version installed
                         glob.glob('/usr/local/Cellar/libmagic/*/lib/libmagic.dylib'),
                       'win32':  ['magic1.dll','cygmagic-1.dll']}
    for dll in platform_to_lib.get(sys.platform, []):
        try:
            libmagic = ctypes.CDLL(dll)
            break
        except OSError:
            pass

if not libmagic or not libmagic._name:
    # It is better to raise an ImportError since we are importing magic module
    raise ImportError('failed to find libmagic.  Check your installation')

magic_t = ctypes.c_void_p

def errorcheck_null(result, func, args):
    if result is None:
        err = magic_error(args[0])
        raise MagicException(err)
    else:
        return result

def errorcheck_negative_one(result, func, args):
    if result is -1:
        err = magic_error(args[0])
        raise MagicException(err)
    else:
        return result


def coerce_filename(filename):
    if filename is None:
        return None

    # ctypes will implicitly convert unicode strings to bytes with
    # .encode('ascii').  If you use the filesystem encoding 
    # then you'll get inconsistent behavior (crashes) depending on the user's
    # LANG environment variable
    is_unicode = (sys.version_info[0] <= 2 and
                  isinstance(filename, unicode)) or \
                  (sys.version_info[0] >= 3 and
                   isinstance(filename, str))
    if is_unicode:
        return filename.encode('utf-8')
    else:
        return filename

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
_magic_file.errcheck = errorcheck_null

def magic_file(cookie, filename):
    return _magic_file(cookie, coerce_filename(filename))

_magic_buffer = libmagic.magic_buffer
_magic_buffer.restype = c_char_p
_magic_buffer.argtypes = [magic_t, c_void_p, c_size_t]
_magic_buffer.errcheck = errorcheck_null

def magic_buffer(cookie, buf):
    return _magic_buffer(cookie, buf, len(buf))


_magic_load = libmagic.magic_load
_magic_load.restype = c_int
_magic_load.argtypes = [magic_t, c_char_p]
_magic_load.errcheck = errorcheck_negative_one

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



MAGIC_NONE = 0x000000 # No flags

MAGIC_DEBUG = 0x000001 # Turn on debugging

MAGIC_SYMLINK = 0x000002 # Follow symlinks

MAGIC_COMPRESS = 0x000004 # Check inside compressed files

MAGIC_DEVICES = 0x000008 # Look at the contents of devices

MAGIC_MIME = 0x000010 # Return a mime string

MAGIC_MIME_ENCODING = 0x000400 # Return the MIME encoding

MAGIC_CONTINUE = 0x000020 # Return all matches

MAGIC_CHECK = 0x000040 # Print warnings to stderr

MAGIC_PRESERVE_ATIME = 0x000080 # Restore access time on exit

MAGIC_RAW = 0x000100 # Don't translate unprintable chars

MAGIC_ERROR = 0x000200 # Handle ENOENT etc as real errors

MAGIC_NO_CHECK_COMPRESS = 0x001000 # Don't check for compressed files

MAGIC_NO_CHECK_TAR = 0x002000 # Don't check for tar files

MAGIC_NO_CHECK_SOFT = 0x004000 # Don't check magic entries

MAGIC_NO_CHECK_APPTYPE = 0x008000 # Don't check application type

MAGIC_NO_CHECK_ELF = 0x010000 # Don't check for elf details

MAGIC_NO_CHECK_ASCII = 0x020000 # Don't check for ascii files

MAGIC_NO_CHECK_TROFF = 0x040000 # Don't check ascii/troff

MAGIC_NO_CHECK_FORTRAN = 0x080000 # Don't check ascii/fortran

MAGIC_NO_CHECK_TOKENS = 0x100000 # Don't check ascii/tokens
