#!/bin/sh

# Build the stuff

TAG=dsn-fault-dc
REPO=sysobs

FULL_NAME=${REPO}/rs-cart:${TAG}

docker build . -t ${FULL_NAME}
docker push ${FULL_NAME}
