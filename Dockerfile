FROM python:2.7-alpine

RUN apk --update add musl-dev gcc

RUN pip install --upgrade pip && pip install tornado && pip install pillow==2.6.1

ADD . .

RUN cd python-nats && python setup.py install && cd .. && rm -R ./python-nats

ENTRYPOINT python ./images.py
