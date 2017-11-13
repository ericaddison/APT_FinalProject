from source.framework.BaseHandler import BaseHandler

from flask import Flask, jsonify, request

#/usr/local/lib/python2.7/dist-packages/google/auth/__init__.py

import google.auth.transport.requests
import google.oauth2.id_token

HTTP_REQUEST = google.auth.transport.requests.Request()
app = Flask(__name__)

class GetUserInfo(BaseHandler):
    def get(self):



        print "Stuff here"



        # ERROR    2017-11-12 22:08:55,101 webapp2.py:1552] Working outside of request context.
        #
        # This typically means that you attempted to use functionality that needed
        # an active HTTP request.  Consult the documentation on testing for
        # information about how to avoid this problem.


        id_token = flask.request.headers['Authorization'].split(' ').pop()
        print "ID Token: ", id_token

        claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
        if not claims:
            return 'Unauthorized', 401

        #Do stuff here, JSONify it, and return it.
        return 'Success' , 200