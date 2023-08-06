FROM debian:buster-slim

LABEL maintainer="Jeremías Casteglione <jrmsdev@gmail.com>"
LABEL version="19.7.26"

USER root:root
WORKDIR /root

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

COPY etc/sudoers.d/sadm /etc/sudoers.d
RUN chmod 440 /etc/sudoers.d/sadm

ARG SADM_UID=1000
ARG SADM_GID=1000

RUN groupadd -g ${SADM_GID} sadm
RUN useradd -c sadm -m -d /home/sadm -s /bin/bash -g ${SADM_GID} -u ${SADM_UID} sadm

RUN mkdir -p /opt/src/sadm /opt/sadm /etc/opt/sadm

RUN chown -v sadm:sadm /opt/src/sadm /opt/sadm /etc/opt/sadm
RUN chmod -v 750 /opt/src/sadm /opt/sadm /etc/opt/sadm

COPY --chown=sadm:sadm requirements.txt /tmp

USER sadm:sadm
WORKDIR /opt/src/sadm

RUN pip3 install --no-warn-script-location -r /tmp/requirements.txt

RUN rm -rf /home/sadm/.cache/pip
RUN rm -f /tmp/requirements.txt

CMD /bin/bash -i -l
