FROM python:3.7.4

COPY . ./opt/myapp/current

WORKDIR /opt/myapp/current/

RUN apt update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 80

