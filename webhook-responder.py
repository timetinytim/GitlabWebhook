#!/usr/bin/python3

"""
Simple GitLab webhook listener template.

GitLab allows the user to create webhooks to trigger external jobs whenever
certain operations are invoked. This is a very basic template for being able
to handle all possible webhook requests from GitLab.

Parameters
----------
verbose : int
    How verbose we want to be
port : int
    The port to listen on for requests
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import logging

def create_args():
    """
    Sets up the arguments we need to listen for
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', default=0,
                        help='increase output verbosity')
    parser.add_argument('-p', '--port', help='port to listen on', default=8000)

    return parser

def process_push():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('push functionality not implemented')
    ### Your own code goes here ###

def process_tag_push():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('tag_push functionality not implemented')
    ### Your own code goes here ###

def process_issue():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('issue functionality not implemented')
    ### Your own code goes here ###

def process_note():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('note functionality not implemented')
    ### Your own code goes here ###

def process_merge_request():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('merge_request functionality not implemented')
    ### Your own code goes here ###

def process_wiki_page():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('wiki_page functionality not implemented')
    ### Your own code goes here ###

def process_pipeline():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('pipeline functionality not implemented')
    ### Your own code goes here ###

def process_build():
    """
    Process a GitLab "push" operation.
    """
    logging.warn('build functionality not implemented')\
    ### Your own code goes here ###

class GitlabHandler(BaseHTTPRequestHandler):
    """
    Simple HTTP request handler for responding to GitLab webhooks.
    """

    def _set_response(self):
        """
        Sends back an HTTP 200 response
        """

        message = b'OK'
        self.send_response(200)
        self.send_header('Content-type', 'text')
        self.send_header('Content-length', str(len(message)))
        self.end_headers()
        self.wfile.write(message)

    def _process_request(self, request_kind):
        """
        Figures out what kind of request we have, and which function to call
        """

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
        """
        Respond to a POST request (the only request GitLab should be sending)
        """

        # Extract the JSON
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        # Send an OK response
        self._set_response()

        # Parse the JSON
        request = json.loads(data_string)
        logging.info("Got request from project %s", request['project']['name'])

        # Send off to the proper function
        self._process_request(request['object_kind'])

#######################################
#            Main Function            #
#######################################
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
