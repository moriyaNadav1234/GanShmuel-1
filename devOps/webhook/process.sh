#!/bin/bash

echo test $1 >> test.log

ref=$1
branch_name=${ref##refs/heads/}

cd /home/ec2-user/app/

git clone git@github.com:develeapDorZ/GanShmuel.git
cd GanShmuel
git checkout "${branch_name}"
git fetch --prune
git pull

docker compose up -d >> test.log


