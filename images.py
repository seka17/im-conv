# coding: utf-8

import time
import os
import StringIO
import re

import tornado.ioloop
import tornado.gen
from tornado.locks import Semaphore

from nats.io.client import Client as NATS

from PIL import Image, ImageDraw, ImageFont


def create_image(text):
    text = unicode(text, "utf-8")
    # remove odd chars
    text = re.sub('[\'\"`]', '', text)
    # text will go out of cell
    if len(text) > 11:
        text = text[:11]
    print("Text to convert: %s" % text)
    # create black rectangle
    img = Image.new('1', (64, 17), 1)
    draw = ImageDraw.Draw(img)
    # draw white text
    draw.text((0, 3), text, 0, font=ImageFont.truetype('./fonts/arial.ttf', 10))
    output = StringIO.StringIO()
    img.save(output, format='BMP')
    return output.getvalue()


@tornado.gen.coroutine
def main():
    nc = NATS()

    print('Listens nats address %s, subcribes to %s, run %d coroutines at the same time' % (NATS_URI, sub, n))
    while True:
        try:
            options = {"servers": NATS_URI}
            yield nc.connect(**options)
            break
        except:
            time.sleep(2)

    @tornado.gen.coroutine
    def subcribe_proxy(msg):
        yield pool_sema.acquire()
        print ("[Received]: %s" % msg.data)
        data = create_image(msg.data)
        pool_sema.release()
        if data is None:
            yield nc.publish(msg.reply, "error")
        else:
            yield nc.publish(msg.reply, data)

    future = nc.subscribe(sub, "", subcribe_proxy)
    sid = future.result()

if __name__ == "__main__":
    try:
        NATS_URI = [os.environ['NATS']]
    except:
        NATS_URI = ["nats://cs03.xyzrd.com:4222"]

    try:
        n = int(os.environ['NUM'])
    except:
        n = 10

    try:
        sub = os.environ['SUB']
    except:
        sub = "image"

    pool_sema = Semaphore(n)
    main()
    tornado.ioloop.IOLoop.instance().start()
