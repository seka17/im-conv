FROM python:2.7-alpine

RUN apk --update add musl-dev gcc git

RUN pip install --upgrade pip && pip install tornado && pip install pillow==2.6.1

RUN git clone https://github.com/nats-io/python-nats && cd python-nats && python setup.py install

ADD . .

ENTRYPOINT python ./images.py
