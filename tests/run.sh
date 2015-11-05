#!/bin/sh

set -e

# ensure we can use unicode filenames in the test
export LC_ALL=en_US.UTF-8
THISDIR=`dirname $0`
export PYTHONPATH=${THISDIR}/..

python2.6 ${THISDIR}/test.py
python2.7 ${THISDIR}/test.py
python3 ${THISDIR}/test.py
