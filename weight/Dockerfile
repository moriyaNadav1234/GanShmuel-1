FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .
COPY ./in ./in
VOLUME /python-docker  #TODO: delete


ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
