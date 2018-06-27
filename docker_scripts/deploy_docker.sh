#!/bin/bash

image="ogloszenia"

set -x
set +e
sudo docker stop $(docker ps  -f ancestor=${image} -q)
set -e

cd ~/app

tar xvf dockerized.tar
rm dockerized.tar

sudo docker build -t ${image} .

sudo docker run --restart unless-stopped -d -e bstok_env="prod" ${image}
sudo docker run --restart unless-stopped -d -e bstok_env="szeregowki" ${image}

