FROM python:alpine

RUN apk update && \
    apk upgrade && \
    apk add supervisor && \
    apk add bash

COPY requirements/production.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py app.py
COPY config config
COPY start.sh start.sh

ENTRYPOINT ["./start.sh"]
