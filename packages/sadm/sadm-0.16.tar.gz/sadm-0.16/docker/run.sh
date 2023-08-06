#!/usr/bin/env bash
set -eu
TAG=${1:-''}
IMAGE='jrmsdev/sadm'
NAME='sadm'
if test "X${TAG}" != 'X'; then
	shift
	IMAGE="jrmsdev/sadm:${TAG}"
	NAME="sadm${TAG}"
fi
PYPATH=''
if test "${TAG}" = 'dev'; then
	PYPATH='-e PYTHONPATH=/opt/src/sadm'
fi
docker run -it --rm --name=${NAME} \
	--hostname=${NAME} \
	-e PATH=/home/sadm/.local/bin:/usr/local/bin:/usr/bin:/bin \
	-v ${PWD}:/opt/src/sadm \
	${PYPATH} ${IMAGE} $@
exit 0
