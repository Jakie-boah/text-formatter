
FROM python:3.13.3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src/app

RUN mkdir -p /usr/src/app/logs/formatting && \
    mkdir -p /usr/src/app/logs/celery && \
    chmod -R 777 /usr/src/app/logs


COPY requirements.txt requirements.txt


RUN  pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir


COPY .. .
