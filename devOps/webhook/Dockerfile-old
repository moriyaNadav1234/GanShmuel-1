FROM docker/compose:alpine-1.29.2

RUN apk add bash curl git tree

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
RUN mkdir ./logs

COPY ./src ./

COPY ./entry-point.sh /usr/bin/
RUN chmod +x /usr/bin/entry-point.sh

EXPOSE 8086

ENTRYPOINT [ "entry-point.sh" ]
