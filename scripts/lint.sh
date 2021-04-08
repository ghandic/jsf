#!/usr/bin/env bash

set -e
set -x

autoflake -r src --recursive --in-place --remove-all-unused-imports --exclude=__init__.py
isort -rc src
black src --line-length=120
flake8 src
