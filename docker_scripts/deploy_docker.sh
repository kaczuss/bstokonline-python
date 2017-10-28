#!/bin/bash

image="ogloszenia"

set -x
set +e
docker stop $(docker ps  -f ancestor=${image} -q)
set -e

cd /app

tar xvf dockerized.tar
rm dockerized.tar

docker build -t ${image} .

docker run --restart unless-stopped -d -e bstok_env="prod" ${image}
docker run --restart unless-stopped -d -e bstok_env="szeregowki" ${image}

