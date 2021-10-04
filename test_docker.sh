#!/bin/bash

# Test with various versions of ubuntu.  This more or less re-creates the
# Travis CI test environment

set -e

DEFAULT_TARGETS="xenial bionic focal centos7 centos8 archlinux alpine"

TARGETS=${1:-${DEFAULT_TARGETS}}

HERE=`dirname $0`

for i in $TARGETS; do
    TAG="python_magic/${i}:latest"
    docker build -t $TAG -f ${HERE}/test/docker/$i .
    docker run $TAG
done
