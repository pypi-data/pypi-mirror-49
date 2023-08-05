#!/bin/sh -eu
docker build -t sadmtest --network host -f Dockerfile.test .
exit 0
