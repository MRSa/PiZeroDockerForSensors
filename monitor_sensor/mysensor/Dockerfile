FROM alpine:3.17

# -----
ENV PREREQUISITES "alpine-sdk python3-dev gcc"

# ------ Install applications
RUN apk update && \
    apk add --no-cache bash $PREREQUISITES \
            python3 py3-pip py3-smbus i2c-tools \
            --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main \
            --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community \
            --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing
# ------
RUN pip3 install bme680 && \
    pip3 install redis && \
    pip3 install hiredis && \
    mkdir -p /work && \
    apk del --purge $PREREUQISTES && \
    mkdir -p /var/mysensor && \
    chmod 777 /var/mysensor 
# ------

COPY ./bme680entry.py /work/dataentry.py

WORKDIR /work

ENTRYPOINT ["python3"]
CMD ["/work/dataentry.py"]
