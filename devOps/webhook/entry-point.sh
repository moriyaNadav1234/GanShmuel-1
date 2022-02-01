#!/bin/sh

pip install -r ./requirements.txt

export FLASK_APP=main.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=8086 > /dev/null 2>&1

#TODO: if flask run fail - send mail to devOps team!
#We don't need to do this, because this webhook service always works
#We deploy it by manual from very first time
