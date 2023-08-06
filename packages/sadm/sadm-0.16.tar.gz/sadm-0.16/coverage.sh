#!/bin/sh -eu
REPORT=${1:-'term'}
PYTHONPATH=${PWD} pytest --cov=_sadm --cov-report=${REPORT}
exit 0
