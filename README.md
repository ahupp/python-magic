# python-magic
[![PyPI version](https://badge.fury.io/py/python-magic.svg)](https://badge.fury.io/py/python-magic)
[![ci](https://github.com/ahupp/python-magic/actions/workflows/ci.yml/badge.svg)](https://github.com/ahupp/python-magic/actions/workflows/ci.yml)
[![Join the chat at https://gitter.im/ahupp/python-magic](https://badges.gitter.im/ahupp/python-magic.svg)](https://gitter.im/ahupp/python-magic?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

python-magic is a Python interface to the libmagic file type
identification library.  libmagic identifies file types by checking
their headers according to a predefined list of file types. This
functionality is exposed to the command line by the Unix command
`file`.

## Usage

```python
>>> import magic
>>> magic.from_file("testdata/test.pdf")
'PDF document, version 1.2'
# recommend using at least the first 2048 bytes, as less can produce incorrect identification
>>> magic.from_buffer(open("testdata/test.pdf", "rb").read(2048))
'PDF document, version 1.2'
>>> magic.from_file("testdata/test.pdf", mime=True)
'application/pdf'
```

There is also a `Magic` class that provides more direct control,
including overriding the magic database file and turning on character
encoding detection.  This is not recommended for general use.  In
particular, it's not safe for sharing across multiple threads and
will fail throw if this is attempted.

```python
>>> f = magic.Magic(uncompress=True)
>>> f.from_file('testdata/test.gz')
'ASCII text (gzip compressed data, was "test", last modified: Sat Jun 28
21:32:52 2008, from Unix)'
```

You can also combine the flag options:

```python
>>> f = magic.Magic(mime=True, uncompress=True)
>>> f.from_file('testdata/test.gz')
'text/plain'
```

## Installation

The current stable version of python-magic is available on PyPI and
can be installed by running `pip install python-magic`.

Other sources:

- PyPI: http://pypi.python.org/pypi/python-magic/
- GitHub: https://github.com/ahupp/python-magic

This module is a simple wrapper around the libmagic C library, and
that must be installed as well:

### Debian/Ubuntu

```
sudo apt-get install libmagic1
```

### Windows

You'll need DLLs for libmagic.  @julian-r maintains a pypi package with the DLLs, you can fetch it with:

```
pip install python-magic-bin
```

### OSX

- When using Homebrew: `brew install libmagic`
- When using macports: `port install file`

### Troubleshooting

- 'MagicException: could not find any magic files!': some
  installations of libmagic do not correctly point to their magic
  database file.  Try specifying the path to the file explicitly in the
  constructor: `magic.Magic(magic_file="path_to_magic_file")`.

- 'WindowsError: [Error 193] %1 is not a valid Win32 application':
  Attempting to run the 32-bit libmagic DLL in a 64-bit build of
  python will fail with this error.  Here are 64-bit builds of libmagic for windows: https://github.com/pidydx/libmagicwin64.
  Newer version can be found here: https://github.com/nscaife/file-windows.

- 'WindowsError: exception: access violation writing 0x00000000 ' This may indicate you are mixing
  Windows Python and Cygwin Python. Make sure your libmagic and python builds are consistent.


## Bug Reports

python-magic is a thin layer over the libmagic C library.
Historically, most bugs that have been reported against python-magic
are actually bugs in libmagic; libmagic bugs can be reported on their
tracker here: https://bugs.astron.com/my_view_page.php.  If you're not
sure where the bug lies feel free to file an issue on GitHub and I can
triage it.

## Running the tests

We use the `tox` test runner which can be installed with `python -m pip install tox`.

To run tests locally across all available python versions:

```
python -m tox
```

Or to run just against a single version:

```
python -m tox py
```
To run the tests across a variety of linux distributions (depends on Docker):

```
./test/run_all_docker_test.sh
```

## libmagic python API compatibility

The python bindings shipped with libmagic use a module name that conflicts with this package.  To work around this, python-magic includes a compatibility layer for the libmagic API.  See [COMPAT.md](COMPAT.md) for a guide to libmagic / python-magic compatibility.

## Versioning

Minor version bumps should be backwards compatible.  Major bumps are not.

## Author

Written by Adam Hupp in 2001 for a project that never got off the
ground.  It originally used SWIG for the C library bindings, but
switched to ctypes once that was part of the python standard library.

You can contact me via my [website](http://hupp.org/adam) or
[GitHub](http://github.com/ahupp).

## License

python-magic is distributed under the MIT license.  See the included
LICENSE file for details.

I am providing code in the repository to you under an open source license. Because this is my personal repository, the license you receive to my code is from me and not my employer (Facebook).
