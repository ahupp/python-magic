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
encoding dectection.  This is not recommended for general use.  In
particular, it its not safe for sharing across multiple threads and
will fail throw if this is attempted.

## Installation

The current stable version of python-magic is available on pypi and
can be installed by running `pip install python-magic`.

Other sources:

- pypi: http://pypi.python.org/pypi/python-magic/
- github: https://github.com/ahupp/python-magic

### Dependencies

On Windows, you need to download and save the following libraries under
`C:\Windows\System32`:

-   `regex2.dll` from [sourceforge.net/projects/gnuwin32/files/regex/](http://sourceforge.net/projects/gnuwin32/files/regex/)
-   `zlib1.dll` from [sourceforge.net/projects/gnuwin32/files/zlib/](http://sourceforge.net/projects/gnuwin32/files/zlib/)
-   `magic1.dll` from [sourceforge.net/projects/gnuwin32/files/file/](http://sourceforge.net/projects/gnuwin32/files/file/)

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
  them yourself (pleae share docs!), or switch to a 32-bit Python.

## Author

Written by Adam Hupp in 2001 for a project that never got off the
ground.  It origionally used SWIG for the C library bindings, but
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

python-magic is distributed under the [PSF License](http://www.python.org/psf/license/).

