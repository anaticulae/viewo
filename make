#!/usr/bin/bash

CURRENT=$(viewo --version)
RELEASE_TAG="${CAELUM_DOCKER_TEST}/caelum_view_release:${CURRENT}"

docker build -t $RELEASE_TAG --file Production .
