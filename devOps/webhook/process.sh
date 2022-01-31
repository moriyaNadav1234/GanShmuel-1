#!/bin/bash

echo test $1 >> /home/ec2-user/app/test.log

ref=$1
branch_name=${ref##refs/heads/}

cd /home/ec2-user/app/

git clone git@github.com:develeapDorZ/GanShmuel.git >> /home/ec2-user/app/test.log
cd GanShmuel
git checkout "${branch_name}" >> /home/ec2-user/app/test.log
git fetch --prune >> /home/ec2-user/app/test.log
git pull >> /home/ec2-user/app/test.log

docker compose up -d >> /home/ec2-user/app/test.log


