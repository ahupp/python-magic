# python-magic

python-magic is a python interface to the libmagic file type
identification library.  libmagic identifies file types by checking
their headers according to a predefined list of file types. This
functionality is exposed to the command line by the Unix command
`file`.

## Example Usage

    >>> import magic
    >>> magic.from_file("testdata/test.pdf")
    'PDF document, version 1.2'
    >>> magic.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'
    >>> magic.from_file("testdata/test.pdf", mime=True)
    'application/pdf'

## Installation

The current stable version of python-magic is available on pypi and
can be installed by running `pip install python-magic`.

Other sources:

- pypi: http://pypi.python.org/pypi/python-magic/
- github: https://github.com/ahupp/python-magic

### Dependencies on Windows

On Windows, you need to download and save the following libraries under
`C:\Windows\System32`:

-   `regex2.dll` from [sourceforge.net/projects/gnuwin32/files/regex/](http://sourceforge.net/projects/gnuwin32/files/regex/)
-   `zlib1.dll` from [sourceforge.net/projects/gnuwin32/files/zlib/](http://sourceforge.net/projects/gnuwin32/files/zlib/)
-   `magic1.dll` from [sourceforge.net/projects/gnuwin32/files/file/](http://sourceforge.net/projects/gnuwin32/files/file/)

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

