#!/usr/bin/env bash

set -ex

SERVER=${1}

if [ -z "$SERVER" ]; then
    exit 1
fi

PORT=${2}

if [ -z "$PORT" ]; then
    PORT=22
fi

USER=${3}

if [ -z "$USER" ]; then
    USER='root'
fi

scp -P ${PORT} docker_scripts/install-docker.sh ${USER}@${SERVER}:~/

ssh -t -p ${PORT} ${USER}@${SERVER} "./install-docker.sh"
