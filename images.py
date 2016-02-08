# coding: utf-8

import time
import os
import StringIO
import re

import tornado.ioloop
import tornado.gen

from nats.io.client import Client as NATS

from PIL import Image
from PIL import ImageDraw


def create_image(text):
    # strip non alphanumeric characters
    text = re.sub(r'\W+', '', text)
    # text will go out of cell
    if len(text) > 11 or len(text) <= 0:
        return None
    print("Text to convert: %s" % text)
    # create black rectangle
    img = Image.new('1', (64, 17), 1)
    draw = ImageDraw.Draw(img)
    # draw white text
    draw.text((0, 3), text, 0)
    output = StringIO.StringIO()
    img.save(output, format='BMP')
    return output.getvalue()


@tornado.gen.coroutine
def main():
    nc = NATS()

    try:
        NATS_URI = [os.environ['NATS']]
    except:
        NATS_URI = ["nats://127.0.0.1:4222"]
    print NATS_URI

    while True:
        try:
            options = {"servers": NATS_URI}
            yield nc.connect(**options)
            break
        except:
            time.sleep(10)

    @tornado.gen.coroutine
    def subcribe_proxy(msg):
            print ("[Received]: %s" % msg.data)
            data = create_image(msg.data)
            if data is None:
                yield nc.publish(msg.reply, 'error')
            else:
                yield nc.publish(msg.reply, data)

    try:
        topic = os.environ['SUB']
    except:
        topic = "image"
    future = nc.subscribe(topic, "", subcribe_proxy)
    sid = future.result()

if __name__ == "__main__":
    main()
    tornado.ioloop.IOLoop.instance().start()
