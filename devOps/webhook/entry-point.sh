#!/bin/sh

python3 -m venv venv
source venv/bin/activate
pip install flask

export FLASK_APP=main.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=8086 > /dev/null 2>&1

#sh /usr/local/bin/docker-compose-entrypoint.sh
