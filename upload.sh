#!/bin/sh

python3 setup.py clean --all
python3 setup.py sdist bdist_wheel
#python3 -m twine upload dist/*

