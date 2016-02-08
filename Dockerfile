FROM python:2.7-alpine

RUN apk --update add musl-dev gcc

RUN pip install --upgrade pip && pip install tornado && pip install pillow==2.6.1

ADD ./python-nats ./python-nats

RUN cd python-nats && python setup.py install && cd .. && rm -R ./python-nats

ADD ./images.py ./images.py

ENTRYPOINT python ./images.py
