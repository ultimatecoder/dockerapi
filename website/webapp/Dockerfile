FROM python:alpine

# Ensure that Python outputs everything that's printed inside # the application
# rather than buffering it.
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk upgrade && \
    apk add supervisor && \
    apk add bash

# Gunicorn
CMD mkdir -p /etc/gunicorn
COPY config/gunicorn.py /etc/gunicorn/config.py

# Webapp
CMD mkdir -p /srv/webapp
WORKDIR /srv/webapp

# Installing Python dependencies
COPY requirements/production.txt requirements.txt
RUN pip install -r requirements.txt

# Copy Webapp files
COPY containers containers
COPY images images
COPY json_api json_api
COPY __init__.py __init__.py
COPY views.py views.py

ENTRYPOINT ["gunicorn", "--config=/etc/gunicorn/config.py"]
CMD ["webapp:app"]
