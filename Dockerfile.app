FROM python:3.6.5

WORKDIR /app
COPY ./app ./

RUN apt update \
    && pip install -r requirements.txt

EXPOSE 80

