#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import logging

def some_function():
    print("some_function got called")

def create_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', default=0,
                        help='increase output verbosity')
    parser.add_argument('-p', '--port', help='port to listen on', default=8000)

    return parser

def process_push():
    logging.warn('push functionality not implemented')

def process_tag_push():
    logging.warn('tag_push functionality not implemented')

def process_issue():
    logging.warn('issue functionality not implemented')

def process_note():
    logging.warn('note functionality not implemented')

def process_merge_request():
    logging.warn('merge_request functionality not implemented')

def process_wiki_page():
    logging.warn('wiki_page functionality not implemented')

def process_pipeline():
    logging.warn('pipeline functionality not implemented')

def process_build():
    logging.warn('build functionality not implemented')

class GitlabHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        message = b'OK'
        self.send_response(200)
        self.send_header('Content-type', 'text')
        self.send_header('Content-length', str(len(message)))
        self.end_headers()
        self.wfile.write(message)

    def _process_request(self, request_kind):
        # Request type -> function links
        switches = {
            'push':          process_push,
            'tag_push':      process_tag_push,
            'issue':         process_issue,
            'note':          process_note,
            'merge_request': process_merge_request,
            'wiki_page':     process_wiki_page,
            'pipeline':      process_pipeline,
            'build':         process_build
        }

        # Run the correct function for the request type
        func = switches.get(request_kind, lambda: logging.error("Invalid request: %s", request_kind))
        func()

    def do_POST(self):

        # Extract the JSON
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        # Send an OK response
        self._set_response()

        # Parse the JSON
        request = json.loads(data_string)
        logging.info("Got request from project %s", request['project']['name'])

        # Send off to the proper function
        self._process_request(request['object_kind'])

if (__name__ == '__main__'):
    # Get args
    parser = create_args()
    args = parser.parse_args()

    # Set logging level
    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Run the server
    logging.info("Starting httpd...\n")
    httpd = HTTPServer(('', args.port), GitlabHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    logging.info("Stopping httpd...\n")
    httpd.server_close()
