FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends \
                    default-jre \
                    git

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app

ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

CMD [ "tail", "-f", "/dev/null" ]