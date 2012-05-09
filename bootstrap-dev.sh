#!/bin/sh
set -e
rm -rf .virtualenv
mkdir .virtualenv
cd .virtualenv
virtualenv --no-site-packages .
cd ..
.virtualenv/bin/pip install -r requirements/dev.txt
