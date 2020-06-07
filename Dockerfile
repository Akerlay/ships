FROM python:3.8-alpine

RUN apk update && apk add --no-cache gcc musl-dev linux-headers postgresql-dev python3-dev tzdata
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . .
RUN python3 setup.py develop
