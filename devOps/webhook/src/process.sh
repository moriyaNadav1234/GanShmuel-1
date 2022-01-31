### we moved to process.py
### this file is depreciated

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
  
  # ${?} in bash holds the last command error code. if == 0 than excuted ok. if /= 0 > error. 
  # bash commands should run with '-e' = exit on error code. (similar to try/catch)
  docker-compose -f ./data/billing/docker-compose.yml up
  
 if [[ "${?}" != "0" ]]
 then
   echo "$(date) : ERROR! code $?" >> error.log
   
 fi
 
}

function testing() {
  success=true

  get_code

  # TODO: run docker-compose for testing
  # docker-compose up -d >> /app/test.log

  if $success
  then
    echo "Job done" # -> mailing service
  else
    send_notify # -> mailing service - fail msg
  fi
}

function prod_deploy() {
  echo "Do deployment ..."
}

function send_notify() {
  echo "Send email notify ..."
}

if [ $branch_name == 'main' ]
then
  testing
  prod_deploy 

elif [ $branch_name == 'billing' ] || [ $branch_name == 'weight' ]; then
  testing

else
  echo "Do nothing"
fi