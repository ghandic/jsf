#!/usr/bin/env bash

set -e
set -x

bash scripts/test.sh --cov=src/jsf --cov-report html ${@}