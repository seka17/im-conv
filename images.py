# coding: utf-8
import time
import os
import StringIO
import re
from multiprocessing import Queue

import cgi
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from PIL import Image, ImageDraw, ImageFont

class Workers:

    def __init__(self, arg):
        self.pool = Queue()
        for _ in xrange(arg):
            self.pool.put(True)

    def do(self, text):
        _ = self.pool.get()
        im = create_image(text)
        # self.func.task_done()
        self.pool.put(True)
        return im

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
    draw.text((0, 3), text, 0, font=ImageFont.truetype(
        './fonts/arial.ttf', 10))
    output = StringIO.StringIO()
    img.save(output, format='BMP')
    return output.getvalue()


class ServerHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        text = form["str"].value
        self.send_response(200)
        self.end_headers()
        self.wfile.write(workers.do(text))
        self.wfile.close()
        return

try:
    number = os.environ['NUM']
except:
    number = 10

workers = Workers(number)

def main():

    PORT = 4655
    httpd = HTTPServer(("", PORT), ServerHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
