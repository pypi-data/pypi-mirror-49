#!/bin/sh -eu
docker run --rm --net=host --name=sadmtest \
	-e PYTHONPATH=/opt/src/sadm \
	-v ${PWD}/docker/bin:/opt/sadm/bin \
	-v ${PWD}/docker/etc:/etc/opt/sadm \
	-v ${PWD}:/opt/src/sadm sadmtest $@
exit 0
