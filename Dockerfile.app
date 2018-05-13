FROM python:3.6.5

WORKDIR /app

COPY ./VERSION ./
COPY ./requirements.txt ./
COPY ./src ./src
COPY ./tasks ./tasks
COPY ./tasks.py ./
COPY ./uwsgi.yml ./

RUN apt update \
    && apt install -y python3-coverage \
    && pip install -r requirements.txt

EXPOSE 80

