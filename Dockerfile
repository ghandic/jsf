FROM python:3.8

WORKDIR /opt/working
COPY . .
RUN pip install .