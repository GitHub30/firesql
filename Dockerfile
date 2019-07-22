FROM mysql:8

ENV DEBIAN_FRONTEND noninteractive
ENV MYSQL_ROOT_PASSWORD root

RUN set -xe \
    && apt-get update \
    && apt-get install -y locales \
    && echo 'ja_JP.UTF-8 UTF-8' > /etc/locale.gen \
    && locale-gen ja_JP.UTF-8 \
    && dpkg-reconfigure locales \
    && /usr/sbin/update-locale LANG=ja_JP.UTF-8

ENV LC_ALL ja_JP.UTF-8

ADD https://gist.githubusercontent.com/GitHub30/ba72f572477144a2e05f55f499c62861/raw/113a1daa222739270a45abe113845547a647e449/firesql.cnf /etc/mysql/conf.d/

# https://stackoverflow.com/questions/40184788/protocol-not-found-socket-getprotobyname
RUN set -xe \
    && apt-get update \
    && apt-get install -y python3-pip git \
    && apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall netbase \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir python-socketio eventlet \
    && git clone https://github.com/howmp/python-mysql-replication \
    && cd python-mysql-replication \
    && python3 setup.py install

RUN set -xe \
    && cd \
    && git clone https://github.com/GitHub30/python-mysql-replication ~/firesql

ENV MYSQL_DATABASE testdb
