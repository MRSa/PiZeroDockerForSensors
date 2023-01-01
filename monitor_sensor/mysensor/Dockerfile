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
RUN pip3 install bme680 smbus smbus2 pimoroni-sgp30 && \
    pip3 install redis && \
    pip3 install hiredis && \
    mkdir -p /work && \
    apk del --purge $PREREUQISTES && \
    mkdir -p /var/mysensor && \
    chmod 777 /var/mysensor 
# ------

COPY ./my-sensor-scan.py /work/my-sensor-scan.py
COPY ./bme680entry.py /work/bme680entry.py
COPY ./mySGP30.py /work/mySGP30.py
COPY ./mySHT31d.py /work/mySHT31d.py
COPY ./myCCS811.py /work/myCCS811.py
COPY ./myBME280.py /work/myBME280.py
COPY ./myBME680.py /work/myBME680.py

WORKDIR /work

ENTRYPOINT ["python3"]
#CMD ["/work/my-sensor-scan.py"]
CMD ["/work/bme680entry.py"]
