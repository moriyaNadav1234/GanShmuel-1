#!/bin/sh

pip3 install -r requirements.txt
python -m pip install mysql-connector-python
python -m pip install openpyxl
flask run --host 0.0.0.0