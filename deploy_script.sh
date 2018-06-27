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

find . -name "*.py" -o -name "*.txt" -o -name "Dockerfile" -o -name ".dockerignore" -o -name "run.sh" | tar -cf dockerized.tar -T -
ssh ${USER}@${SERVER} -p ${PORT} "mkdir -p ~/app"
scp -P ${PORT} dockerized.tar ${USER}@${SERVER}:~/app/.
scp -P ${PORT} docker_scripts/deploy_docker.sh ${USER}@${SERVER}:~/
rm dockerized.tar

ssh -t ${USER}@${SERVER} -p ${PORT} "~/deploy_docker.sh"
