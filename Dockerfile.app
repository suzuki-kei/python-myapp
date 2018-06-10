FROM python:3.6.5

COPY . ./opt/myapp/current

WORKDIR /opt/myapp/current/

RUN apt update \
    && pip install -r requirements.txt

EXPOSE 80

