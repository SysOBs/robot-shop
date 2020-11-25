#!/bin/sh

# Build the stuff

TAG=dsn
REPO=sysobs

FULL_NAME=${REPO}/rs-load:${TAG}

docker build . -t ${FULL_NAME}
docker push ${FULL_NAME}
