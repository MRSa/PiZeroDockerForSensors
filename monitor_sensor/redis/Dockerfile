FROM alpine:3.17

EXPOSE 6379

ENV REDIS_VERSION="redis-6.2.8"
ENV REDIS_TIMESERIES_VERSION="1.4"
ENV PREREQUISITES "alpine-sdk make gcc git g++ automake curl autoconf pkgconf lcov"

# -----
COPY ./redis.conf /etc/redis/redis.conf

# ------ Install prerequisites
RUN apk update && \
    apk add --no-cache $PREREQUISITES bash libffi-dev \
        --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing 
# ------
#  https://redis.io/
RUN  mkdir /tmp/redis && \
     cd /tmp/redis && \ 
     curl -fsSL http://download.redis.io/releases/${REDIS_VERSION}.tar.gz | tar zxvf - && \
     cd ${REDIS_VERSION} && \
     make && \
     make install && \
     ls -l /usr/local/bin && \
     mkdir /usr/local/redis && \
     ls -l /usr/local/redis
# ------
#  https://github.com/RedisTimeSeries/RedisTimeSeries
RUN mkdir /tmp/redisTimeSeries && \
    cd /tmp/redisTimeSeries && \
    git clone --recursive https://github.com/RedisTimeSeries/RedisTimeSeries.git -b ${REDIS_TIMESERIES_VERSION} && \
    cd RedisTimeSeries && \
    make setup && \
    make build && \
    cp -a bin/* /usr/local/redis/ && \
    ls -l /usr/local/redis && \
    ls -l /etc/redis  && \
    rm -rf /tmp/* && \
    apk del --purge $PREREUQISTES && \
    mkdir /var/redis && \
    chmod 777 /var/redis 

WORKDIR /var/redis

ENTRYPOINT ["/usr/local/bin/redis-server"]
CMD ["/etc/redis/redis.conf"]
