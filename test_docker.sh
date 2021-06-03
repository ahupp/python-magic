#!/bin/bash

# Test with various versions of ubuntu.  This more or less re-creates the
# Travis CI test environment

set -e

NAME=`basename $1`
TAG="python_magic/${NAME}:latest"
docker build -t $TAG -f $1 .
docker run $TAG

