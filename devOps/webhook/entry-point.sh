#!/bin/sh

# python3 -m venv venv #why creating virtual enviroment inside a container?! it is already a controlled virtual enviroment !?
# source venv/bin/activate
# pip install flask #need to use requierments.txt! 

export FLASK_APP=main.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=8086 > /dev/null 2>&1

#TODO: if flask run fail - send mail to devOps team! 

#sh /usr/local/bin/docker-compose-entrypoint.sh