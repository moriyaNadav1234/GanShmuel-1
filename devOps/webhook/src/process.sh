#!/bin/bash

ref=$1
branch_name=${ref##refs/heads/}

echo "ref $1" >> /app/test.log
echo "branch $branch_name" >> /app/test.log

function get_code() {
  #git clone git@github.com:develeapDorZ/GanShmuel.git >> /app/test.log
  #cd GanShmuel
  #git checkout "${branch_name}" >> /app/test.log
  #git fetch --prune >> /app/test.log
  #git pull >> /app/test.log

  docker-compose -f /data/billing/docker-compose.yml up
}

function testing() {
  success=true

  get_code

  # TODO: run docker-compose for testing
  # docker-compose up -d >> /app/test.log

  if $success
  then
    echo "Job done"
  else
    send_notify
  fi
}

function prod_deploy() {
  echo "Do deployment ..."
}

function send_notify() {
  echo "Send email notify ..."
}

if [ $branch_name == 'main' ]; then
  testing
  prod_deploy

elif [ $branch_name == 'billing' ] || [ $branch_name == 'weight' ]; then
  testing

else
  echo "Do nothing"
