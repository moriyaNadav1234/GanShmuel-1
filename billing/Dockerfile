FROM python:alpine3.14
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . /billing
WORKDIR /billing
RUN pip3 install -r requirements.txt
RUN python -m pip install mysql-connector-python
RUN python -m pip install openpyxl
RUN python -m pip install requests
RUN pip install xlwt
ENTRYPOINT [ "flask" , "run" ]