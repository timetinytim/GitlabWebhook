#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def some_function():
    print("some_function got called")

class MyHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        message = b'OK'
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.send_header("Content-length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)

    def do_POST(self):

        # Extract the JSON
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        # Send an OK response
        self._set_response()

        # Parse the JSON
        text = json.loads(data_string)

        # Make sure it's what we want
        if (text['project']['name'] != 'pfc-2019-website') :
            print("Unknown project: %s" % text.project.name)
            exit(1)

        # We are looking for completed merge requests
        if (text['object_kind'] == 'merge_request' and
            text['changes']['state']['current'] == 'merged'):

            # Need to invoke things
            print("awesome")

        if self.path == '/captureImage':
            # Insert your code here
            some_function()

httpd = HTTPServer(('', 8000), MyHandler)
httpd.serve_forever()