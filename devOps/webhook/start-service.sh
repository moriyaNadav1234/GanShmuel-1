#!/bin/bash

cd /home/ec2-user/app/

python3 -m venv venv >> /tmp/flask.log
source venv/bin/activate >> /tmp/flask.log
pip install flask >> /tmp/flask.log

export FLASK_APP=main.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=8086 >> /tmp/flask.log
