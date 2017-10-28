#!/usr/bin/env bash

set -ex

SERVER=${1}

if [ -z "$SERVER" ]; then
    exit 1
fi


find . -name "*.py" -o -name "*.txt" -o -name "Dockerfile" -o -name ".dockerignore" -o -name "run.sh" | tar -cf dockerized.tar -T -
ssh root@${SERVER} "mkdir -p /app"
scp dockerized.tar root@${SERVER}:/app/.
scp docker_scripts/deploy_docker.sh root@${SERVER}:
rm dockerized.tar

ssh -t root@${SERVER} "./deploy_docker.sh"
