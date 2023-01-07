FROM python:3.8 AS builder

WORKDIR /opt/working
COPY . .
RUN make build

FROM python:3.8.16-alpine3.17 
WORKDIR /root/
COPY --from=builder /opt/working/dist/jsf-*.tar.gz ./
RUN pip install /root/jsf-*.tar.gz
CMD ["jsf"]  