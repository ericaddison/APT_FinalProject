import requests as req
import json
from pprint import pprint
# demos of calling the web API

def process_response(url, r):
    rdict = json.loads(r.content)
    print("Response from {}".format(url))
    pprint(rdict)
    return rdict

# make a new conversation
url = 'http://localhost:8080/api/conversations/'
r = req.post(url, data={"conv_name": "Demo Conversation2"})
print(r)
r0 = process_response(url, r)
conv_id = r0['conversations']['id']

# retrieve that conversation
url = 'http://localhost:8080/api/conversations/{}'.format(conv_id)
r = req.get(url)
process_response(url, r)

# get the users from that conversation
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url)
process_response(url, r)

# post a message to that conversation
# TODO: change message post to accept request data and get user alias
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.post(url, data={"text": "I am a message", "media_url": "http://www.google.com"})
process_response(url, r)

# get the messages from that conversation
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.get(url)
process_response(url, r)