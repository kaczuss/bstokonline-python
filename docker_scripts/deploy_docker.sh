#!/bin/bash

set -x
set +e
docker stop $(docker ps  -f ancestor=ogloszenia -q)
set -e

cd /app

tar xvf dockerized.tar
rm dockerized.tar

docker build -t ogloszenia .

docker run -d -e bstok_env='prod' ogloszenia

