FROM alpine:3.7 as base

FROM base as build
RUN mkdir -p /install
WORKDIR /install

COPY requirements-proxy.txt /requirements.txt

# Install all the dev libraries under the sun to compile custom modules
# Remove useless docs directory ./share
# Remove cached files, they'll get recreated anyway.
RUN apk update && \
    apk add --no-cache python3 ca-certificates gcc musl-dev linux-headers python3-dev make libffi-dev openssl-dev g++ libtool m4 libuv-dev automake autoconf py3-cryptography && \
    python3 -m ensurepip && \
    pip3 install --install-option="--prefix=/install" -r /requirements.txt && \
    rm -rf /install/share && \
    find /install | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

FROM base

COPY --from=build /install /usr

WORKDIR /app/

# Install only the shared libraries that are needed by ldd'ing the .so files
# Find missing libs
# find /usr/local/lib/python3.6/site-packages -iname '*.so' -exec ldd {} \; 2>&1| grep 'Error loading shared library' | awk '{print $5}' | sort -u
RUN apk update && \
    apk add --no-cache python3 ca-certificates py3-cryptography && \
    rm -rf /var/cache/apk/*

COPY metadata_proxy /app/metadata_proxy

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

ENTRYPOINT ["python3", "/app/metadata_proxy/server.py"]
