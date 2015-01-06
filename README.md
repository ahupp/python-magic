# python-magic

python-magic is a python interface to the libmagic file type
identification library.  libmagic identifies file types by checking
their headers according to a predefined list of file types. This
functionality is exposed to the command line by the Unix command
`file`.

## Usage

    >>> import magic
    >>> magic.from_file("testdata/test.pdf")
    'PDF document, version 1.2'
    >>> magic.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'
    >>> magic.from_file("testdata/test.pdf", mime=True)
    'application/pdf'

There is also a `Magic` class that provides more direct control,
including overriding the magic database file and turning on character
encoding detection.  This is not recommended for general use.  In
particular, it's not safe for sharing across multiple threads and
will fail throw if this is attempted.

    >>> f = magic.Magic(uncompress=True)
    >>> f.from_file('testdata/test.gz')
    'ASCII text (gzip compressed data, was "test", last modified: Sat Jun 28
    21:32:52 2008, from Unix)'

You can also combine the flag options:

    >>> f = magic.Magic(mime=True, uncompress=True)
    >>> f.from_file('testdata/test.gz')
    'text/plain'

## Name Conflict

There are, sadly, two libraries which use the module name `magic`.  Both have been around for quite a while.If you are using this module and get an error using a method like `open`, your code is expecting the other one.  Hopefully one day these will be recociled.

## Installation

The current stable version of python-magic is available on pypi and
can be installed by running `pip install python-magic`.

Other sources:

- pypi: http://pypi.python.org/pypi/python-magic/
- github: https://github.com/ahupp/python-magic

### Dependencies

On Windows, install Cygwin (http://cygwin.com/install.html).  To find
the libraries, either add <your-cygwin-install>/bin to the $PATH or
copy cygwin1.dll, cygz.dll, and cygmagic-1.dll to C:\Windows\System32

On OSX:

- When using Homebrew: `brew install libmagic`
- When using macports: `port install file`

### Troubleshooting

- 'MagicException: could not find any magic files!': some
  installations of libmagic do not correctly point to their magic
  database file.  Try specifying the path to the file explictly in the
  constructor: `magic.Magic(magic_file="path_to_magic_file")`.

- 'WindowsError: [Error 193] %1 is not a valid Win32 application':
  Attempting to run the 32-bit libmagic DLL in a 64-bit build of
  python will fail with this error.  I'm not aware of any publically
  available 64-bit builds of libmagic.  You'll either need to build
  them yourself (please share docs!), or switch to a 32-bit Python.

## Author

Written by Adam Hupp in 2001 for a project that never got off the
ground.  It originally used SWIG for the C library bindings, but
switched to ctypes once that was part of the python standard library.

You can contact me via my [website](http://hupp.org/adam) or
[github](http://github.com/ahupp).

## Contributors

Thanks to these folks on github who submitted features and bugfixes.

-   Amit Sethi
-   [bigben87](https://github.com/bigben87)
-   [fallgesetz](https://github.com/fallgesetz)
-   [FlaPer87](https://github.com/FlaPer87)
-   [lukenowak](https://github.com/lukenowak)
-   NicolasDelaby
-   sacha@ssl.co.uk
-   SimpleSeb
-   [tehmaze](https://github.com/tehmaze)

## License

python-magic is distributed under the MIT license.  See the included
LICENSE file for details.

