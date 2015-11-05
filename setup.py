#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='python-magic',
      description='File type identification using libmagic',
      author='Adam Hupp',
      author_email='adam@hupp.org',
      url="http://github.com/ahupp/python-magic",
      version='0.4.10',
      py_modules=['magic'],
      long_description="""This module uses ctypes to access the libmagic file type
identification library.  It makes use of the local magic database and
supports both textual and MIME-type output.
""",
      keywords="mime magic file",
      license="PSF",
      test_suite='tests',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
      ],
      )
