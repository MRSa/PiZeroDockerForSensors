ARG BASE_IMAGE=alpine:3.17
FROM ${BASE_IMAGE}

# ----- grafana image -----
#ARG GRAFANA_TGZ="grafana-8.3.3.linux-armv6.tar.gz"
ARG GRAFANA_TGZ="grafana-9.3.2.linux-armv6.tar.gz"

# Make sure we have Gnu tar
RUN apk add --no-cache tar wget

RUN wget https://dl.grafana.com/oss/release/${GRAFANA_TGZ} -O /tmp/grafana.tar.gz

# Change to tar xfzv to make tar print every file it extracts
RUN mkdir /tmp/grafana && tar xzf /tmp/grafana.tar.gz --strip-components=1 -C /tmp/grafana

FROM ${BASE_IMAGE}

ARG GF_UID="472"
ARG GF_GID="0"

ENV PATH=/usr/share/grafana/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    GF_PATHS_CONFIG="/etc/grafana/grafana.ini" \
    GF_PATHS_DATA="/var/lib/grafana" \
    GF_PATHS_HOME="/usr/share/grafana" \
    GF_PATHS_LOGS="/var/log/grafana" \
    GF_PATHS_PLUGINS="/var/lib/grafana/plugins" \
    GF_PATHS_PROVISIONING="/etc/grafana/provisioning" \
    GF_INSTALL_PLUGINS="redis-app,redis-explorer-app"


WORKDIR $GF_PATHS_HOME

RUN apk add --no-cache ca-certificates bash tzdata && \
    apk add --no-cache musl-utils musl libc6-compat

RUN apk add --no-cache openssl --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main

COPY --from=0 /tmp/grafana "$GF_PATHS_HOME"

RUN if [ ! $(getent group "$GF_GID") ]; then \
      addgroup -S -g $GF_GID grafana; \
    fi

COPY ./run.sh /run.sh
RUN export GF_GID_NAME=$(getent group $GF_GID | cut -d':' -f1) && \
    mkdir -p "$GF_PATHS_HOME/.aws" && \
    adduser -S -u $GF_UID -G "$GF_GID_NAME" grafana && \
    mkdir -p "$GF_PATHS_PROVISIONING/datasources" \
             "$GF_PATHS_PROVISIONING/dashboards" \
             "$GF_PATHS_PROVISIONING/notifiers" \
             "$GF_PATHS_PROVISIONING/plugins" \
             "$GF_PATHS_PROVISIONING/access-control" \
             "$GF_PATHS_LOGS" \
             "$GF_PATHS_PLUGINS" \
             "$GF_PATHS_DATA" && \
    cp "$GF_PATHS_HOME/conf/sample.ini" "$GF_PATHS_CONFIG" && \
    cp "$GF_PATHS_HOME/conf/ldap.toml" /etc/grafana/ldap.toml && \
    chown -R "grafana:$GF_GID_NAME" "$GF_PATHS_DATA" "$GF_PATHS_HOME/.aws" "$GF_PATHS_LOGS" "$GF_PATHS_PLUGINS" "$GF_PATHS_PROVISIONING" && \
    chmod -R 777 "$GF_PATHS_DATA" "$GF_PATHS_HOME/.aws" "$GF_PATHS_LOGS" "$GF_PATHS_PLUGINS" "$GF_PATHS_PROVISIONING" && \
    chmod a+rx /run.sh

EXPOSE 3000

USER "$GF_UID"
ENTRYPOINT [ "/run.sh" ]

