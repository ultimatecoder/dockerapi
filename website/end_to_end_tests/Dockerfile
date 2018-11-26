FROM python:alpine

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN mkdir -p /srv/end_to_end_tests

WORKDIR /srv/end_to_end_tests

COPY api_tests api_tests

ENTRYPOINT ["py.test", "-vv", "--tavern-strict", "body", "--", "api_tests"]
