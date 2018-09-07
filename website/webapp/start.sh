#! /bin/bash

exec gunicorn -c config/gunicorn.py app:app
