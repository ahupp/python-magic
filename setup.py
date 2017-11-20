#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='python-magic',
      description='File type identification using libmagic',
      author='Adam Hupp',
      author_email='adam@hupp.org',
      url="http://github.com/ahupp/python-magic",
      version='0.4.15',
      py_modules=['magic'],
      long_description="""This module uses ctypes to access the libmagic file type
identification library.  It makes use of the local magic database and
supports both textual and MIME-type output.
""",
      keywords="mime magic file",
      license="MIT",
      test_suite='test',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      )
