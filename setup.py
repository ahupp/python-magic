#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import io
import os


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

setuptools.setup(
    name='python-magic',
    description='File type identification using libmagic',
    author='Adam Hupp',
    author_email='adam@hupp.org',
    url="http://github.com/ahupp/python-magic",
    version='0.4.27',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['magic'],
    package_data={
        'magic': ['py.typed', '*.pyi', '**/*.pyi'],
    },
    keywords="mime magic file",
    license="MIT",
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

