FROM python:2.7.11-alpine

RUN apk add --update-cache bash build-base zlib zlib-dev curl jpeg jpeg-dev libpng libpng-dev git freetype freetype-dev

# To fix following error: IOError: decoder zip not available
RUN ln -s /lib/libz.so /usr/lib/

RUN pip install --upgrade pip && pip install tornado && pip install pillow==2.6.1

RUN git clone https://github.com/nats-io/python-nats && cd python-nats && python setup.py install && cd .. && rm -R python-nats

WORKDIR /

ADD . .

ENTRYPOINT python ./images.py
