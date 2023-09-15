#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import io
import os
import sys

# python packages should not install succesfully if libraries are missing
from magic.loader import load_lib
lib = load_lib()._name

def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

def get_cmdclass():
    """Build a platform-specific wheel when `setup.py bdist_wheel` is called."""
    if sys.version_info[0] == 2:
        return {}

    try:
        from wheel.bdist_wheel import bdist_wheel
    except ImportError:
        return {}

    class bdist_wheel_platform_specific(bdist_wheel):
        def get_tag(self):
            python, abi, _ = super().get_tag()
            # get the platform tag based on libmagic included in this wheel
            self.root_is_pure = False
            _, _, plat = super().get_tag()
            return python, abi, plat

    return {"bdist_wheel": bdist_wheel_platform_specific}

cmdclass = get_cmdclass()

setuptools.setup(
    name='python-magic',
    description='File type identification using libmagic',
    author='Adam Hupp',
    author_email='adam@hupp.org',
    url="http://github.com/ahupp/python-magic",
    version='0.4.28',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['magic'],
    package_data={
        'magic': ['py.typed', '*.pyi', '*.dylib*', '*.dll', '*.so*', 'magic.mgc']
    },
    cmdclass=cmdclass,
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
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

