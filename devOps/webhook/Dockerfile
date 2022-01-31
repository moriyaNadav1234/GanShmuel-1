#FROM docker/compose:1.24.1
FROM docker/compose:alpine-1.29.2

RUN apk add bash curl git

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app

COPY ./src ./

COPY ./entry-point.sh /usr/bin/
RUN chmod +x /usr/bin/entry-point.sh

EXPOSE 8086

#ENTRYPOINT ["sh" "/usr/local/bin/docker-compose-entrypoint.sh"]
ENTRYPOINT [ "entry-point.sh" ]
#CMD ["/bin/sh"]
