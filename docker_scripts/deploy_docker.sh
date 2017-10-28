#!/bin/bash

VERSION=${1}
if [ "$VERSION" = "prod" ]; then
	image="ogloszenia"
elif [ "$VERSION" = "szeregowki" ]; then
	image="szeregowki"
else
	echo "Choose version: prod, szeregowki"
	exit 1
fi


set -x
set +e
docker stop $(docker ps  -f ancestor=${image} -q)
set -e

cd /app

tar xvf dockerized.tar
rm dockerized.tar

docker build -t ${image} .

docker run --restart unless-stopped -d -e bstok_env="$1" ${image}

