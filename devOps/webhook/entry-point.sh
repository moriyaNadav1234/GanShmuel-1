#!/bin/sh

pip install -r ./requirements.txt #should move to Dockerfile - RUN

export FLASK_APP=main.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=8086 #> /dev/null 2>&1