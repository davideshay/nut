FROM alpine:edge

MAINTAINER David Shay

# 'nut' package is only available from testing branch -- add it to the repo list
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk add --no-cache nut kubectl curl jq

# rename included config files to .sample, bail out with failure if /etc/nut would not exist
# RUN [ -d /etc/nut ] && find /etc/nut/ -type f -exec mv {} {}.sample \; || false

COPY files/*.sh /

COPY files/etc/nut /etc/nut

RUN chmod 700 /*.sh

RUN mkdir -p /var/run/nut && \
    chown nut:nut /var/run/nut && \
    chmod 700 /var/run/nut && \
    chown -R nut:nut /etc/nut && \
    chmod -R 0440 /etc/nut

ENTRYPOINT ["/startup.sh"]

EXPOSE 3493
