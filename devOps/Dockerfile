FROM docker/compose:debian-1.29.2

RUN apt-get update -y
#RUN apt-get install software-properties-common -y
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev -y
RUN cd /tmp/ && \
    wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz && \
    tar -xf Python-3.7.4.tgz && \
    cd Python-3.7.4 && \
    ./configure --enable-optimizations && \
    make -j 8 && \
    make altinstall

WORKDIR /app


# Temporary stop this
# We dont allow it run for now 
# Because we're trying to debug our Dockerfile
# ENTRYPOINT ["python3 app.py"]
