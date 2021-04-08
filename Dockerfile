FROM python:3.8

WORKDIR /tmp
COPY . .
RUN pip install .