FROM python:rc-alpine

RUN set -xe \
    && apk add --no-cache --virtual .build-deps git gcc musl-dev \
    && pip3 install --no-cache-dir python-socketio eventlet flask flask-cors \
    && git clone https://github.com/howmp/python-mysql-replication \
    && cd python-mysql-replication \
    && python setup.py install \
    && cd .. \
    && rm -rf python-mysql-replication \
    && apk del .build-deps

COPY *.py /root/

CMD ["python", "/root/firesql.py"]
