#!/usr/bin/env bash

set -ex

SERVER=${1}

if [ -z "$SERVER" ]; then
    exit 1
fi

scp docker_scripts/install-docker.sh root@${SERVER}:

ssh -t root@${SERVER} "./install-docker.sh"
