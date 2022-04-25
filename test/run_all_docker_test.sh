#!/bin/sh

set -e
set -x

ROOT=$(dirname $0)/..
cd $ROOT

for f in test/docker/*; do 
    H=$(docker build -q -f ${f} .)
    docker run --rm $H
done

