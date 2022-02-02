#!/bin/bash

docker network create -d bridge billingServ-network 2>/dev/null
docker run -dit --net billingServ-network --name apiService -p 5001:5000 -v $PWD:/billing python:alpine3.14
docker run --net billingServ-network -v $PWD/db:/db --name billingDB -e MYSQL_ROOT_PASSWORD=catty -d mysql:8.0
