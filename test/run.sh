#!/bin/sh

set -e;

# ensure we can use unicode filenames in the test
export LC_ALL=en_US.UTF-8
THISDIR=`dirname $0`
export PYTHONPATH=${THISDIR}/..

PYTHONS="python2.7 python3.5"

for pyver in $PYTHONS; do
    if which $pyver > /dev/null; then
        echo "found $pyver"
        $pyver ${THISDIR}/test.py
    else
        echo "version $pyver not found"
    fi
done
