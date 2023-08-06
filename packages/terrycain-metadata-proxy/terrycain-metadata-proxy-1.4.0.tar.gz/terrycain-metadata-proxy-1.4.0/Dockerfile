FROM alpine:3.7 as base

FROM base as build
RUN mkdir -p /install
WORKDIR /install

RUN apk update && \
    apk add --no-cache python3 ca-certificates py3-cryptography && \
    apk add --no-cache gcc musl-dev linux-headers python3-dev make libffi-dev openssl-dev g++ libtool m4 libuv-dev automake autoconf  && \
    pip3 install terrycain-metadata-proxy && \
    apk del gcc musl-dev linux-headers python3-dev make libffi-dev openssl-dev g++ libtool m4 libuv-dev automake autoconf && \
    rm -rf /var/cache/apk/*

COPY metadata_proxy /app/metadata_proxy

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENTRYPOINT ["python3", "/app/metadata_proxy/server.py"]
