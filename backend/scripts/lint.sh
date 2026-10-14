#!/usr/bin/env bash

set -e
set -x

mypy app
ty check app
ruff check app tests
ruff format app tests --check
