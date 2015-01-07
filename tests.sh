#!/bin/sh

set -e

# ensure we can use unicode filenames in the test
export LC_ALL=en_US.UTF-8

python2.6 test.py
python2.7 test.py
python3 test.py
