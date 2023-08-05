FROM debian:stable-slim

LABEL maintainer="Jeremías Casteglione <jrmsdev@gmail.com>"
LABEL version="19.6.24"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get clean
RUN apt-get update

RUN apt-get dist-upgrade -y --purge
RUN apt-get install -y --no-install-recommends sudo python3 python3-pip

RUN apt-get clean
RUN apt-get autoremove -y --purge

RUN rm -rf /var/lib/apt/lists/*
RUN rm -f /var/cache/apt/archives/*.deb
RUN rm -f /var/cache/apt/*cache.bin

RUN mkdir -p /opt/sadm
RUN mkdir -p /etc/opt/sadm

RUN useradd -c sadm -m -s /bin/bash -U sadm

RUN chgrp sadm /opt/sadm
RUN chmod g+w /opt/sadm

COPY etc/sudoers.d/sadm /etc/sudoers.d
RUN chmod 440 /etc/sudoers.d/sadm

USER sadm:sadm
WORKDIR /opt/src/sadm
