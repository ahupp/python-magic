#!/bin/bash

# Test with various versions of ubuntu.  This more or less re-creates the
# Travis CI test environment

function TestInContainer {
    local name="$1"
    local TAG="python_magic/${name}:latest"
    docker build -t $TAG -f "test/Dockerfile_${name}" .
    docker run "python_magic/${name}:latest"
}

TestInContainer "xenial"
TestInContainer "bionic"
TestInContainer "focal"

