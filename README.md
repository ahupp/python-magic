# Python Magic

Python Magic is a simple wrapper for libmagic.

## libmagic

libmagic identifies file types by checking their headers according to a
predefined  list of file tyes. This functionality is exposed to the command line
by the Unix command `file`, which uses several methods to determine the type of
a file.

See `/usr/share/misc/magic` for a complete and annotated list of default mappings.

## License

Python Magic is distributed under the [PSF License](http://www.python.org/psf/license/).

## Dependencies on Windows

On Windows, you need to download and save the following libraries under
`C:\Windows\System32`:

-   `regex2.dll` from [sourceforge.net/projects/gnuwin32/files/regex/](http://sourceforge.net/projects/gnuwin32/files/regex/)
-   `zlib1.dll` from [sourceforge.net/projects/gnuwin32/files/zlib/](http://sourceforge.net/projects/gnuwin32/files/zlib/)
-   `magic1.dll` from [sourceforge.net/projects/gnuwin32/files/file/](http://sourceforge.net/projects/gnuwin32/files/file/)

## Downloading

To download Python Magic run:

    git clone git://github.com/ahupp/python-magic.git

You may want to checkout the latest release:

    cd python-magic && git checkout `git describe --abbrev=0 --tags`

## Installation

To build and install Python Magic run:

    cd python-magic && python setup.py install

## Example Usage

    >>> import magic
    >>> m = magic.Magic()
    >>> m.from_file("testdata/test.pdf")
    'PDF document, version 1.2'
    >>> m.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'

### For MIME types

    >>> mime = magic.Magic(mime=True)
    >>> mime.from_file("testdata/test.pdf")
    'application/pdf'
    >>>

### For MIME encoding

    >>> mime_encoding = magic.Magic(mime_encoding=True)
    >>> mime_encoding.from_file("testdata/text-iso8859-1.txt")
    'iso-8859-1'
    >>>

## Autor

Adam Hupp <adam at hupp.org>

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

