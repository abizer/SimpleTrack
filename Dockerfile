FROM python:2.7-alpine
MAINTAINER tahabi <abizer@abizer.me>

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY simpletrack.py /app
COPY static/ /app/static/
COPY templates/ /app/templates/

RUN mkdir /app/socket

CMD gunicorn -w 4 --bind unix:/app/socket/simpletrack.sock simpletrack:app