import requests as req
import json
from pprint import pprint
import random


# demos of calling the web API
#
# What should we be able to do?
# 1) create a conversation (GOOD)
# 2) retrieve conversation details (GOOD)
# 3) Delete a conversation (?)
# 4) Post a message to a conversation (GOOD)
# 5) Retrieve messages from a conversation (GOOD)
# 6) Edit a message in a conversation
# 7) Delete a message in a conversation (GOOD)
# 8) Retrieve list of aliases in a conversation (GOOD)
# 9) Leave a conversation (GOOD)
# 10) Join an existing conversation (GOOD)

# For these demos, make sure source.config.authentication has AUTH_PROVIDER set to auth_demo
# Then, token 'DEVTOKEN1' will access dummy user 1
# and token 'DEVTOKEN2' will access dummy user 2


def process_response(_url, _r):
    rdict = json.loads(_r.content)
    print("Response from {}".format(_url))
    pprint(rdict)
    print("\n")
    return rdict

# set up two authorization headers, one for each dummy user
headers1 = {"Authorization": "Bearer DEVTOKEN1"}
headers2 = {"Authorization": "Bearer DEVTOKEN2"}


# 1) create a conversation
print("Create Conversation")
url = 'http://localhost:8080/api/conversations/'
r = req.post(url, data={"conv_name": "Demo Conversation {}".format(random.randint(0, 1000))}, headers=headers1)
print(r)
r0 = process_response(url, r)
conv_id = r0['conversations']['id']


# 2) retrieve conversation details -- authorized user
print("Get Conversation Info -- Authorized")
url = 'http://localhost:8080/api/conversations/{}'.format(conv_id)
r = req.get(url, headers=headers1)
process_response(url, r)


# 2) retrieve conversation details -- unauthorized user
print("Get Conversation Info -- Unauthorized")
url = 'http://localhost:8080/api/conversations/{}'.format(conv_id)
r = req.get(url, headers=headers2)
process_response(url, r)


# 8) Retrieve list of aliases in a conversation -- authorized user
print("Get Users -- authorized")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url, headers=headers1)
process_response(url, r)


# 8) Retrieve list of aliases in a conversation -- unauthorized user
print("Get Users -- unauthorized")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url, headers=headers2)
process_response(url, r)


# 4) Post a message to a conversation -- authorized
print("Post Message -- authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.post(url, data={"text": "I am a message", "media_url": "http://www.google.com"}, headers=headers1)
process_response(url, r)


# 4) Post a message to a conversation -- unauthorized
print("Post Message -- unauthorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.post(url, data={"text": "I am a message", "media_url": "http://www.google.com"}, headers=headers2)
process_response(url, r)


# 5) Retrieve messages from a conversation -- authorized
print("Get Messages -- authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.get(url, headers=headers1)
process_response(url, r)


# 5) Retrieve messages from a conversation -- unauthorized
print("Get Messages -- unauthorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.get(url, headers=headers2)
process_response(url, r)


# 10) Join an existing conversation
print("Join Conversation")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.post(url, headers=headers2)
process_response(url, r)


# 4) Post a message to a conversation -- now authorized
print("Post Message -- authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.post(url, data={"text": "Now I am authorized!", "media_url": "http://www.google.com"}, headers=headers2)
process_response(url, r)
r1 = process_response(url, r)
msg_id = r1['messages']['id']


# 5) Retrieve messages from a conversation -- now authorized
print("Get Messages -- now authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.get(url, headers=headers2)
process_response(url, r)


# 7) Delete a message from a conversation -- not found
print("Delete Message -- not found")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.delete(url, headers=headers1)
process_response(url, r)


# 7) Delete a message from a conversation -- not authorized
print("Delete Message -- not authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(conv_id, msg_id)
r = req.delete(url, headers=headers1)
process_response(url, r)


# 7) Delete a message from a conversation -- authorized
print("Delete Message -- authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(conv_id, msg_id)
r = req.delete(url, headers=headers2)
process_response(url, r)


# 5) Retrieve messages from a conversation -- now authorized
print("Get Messages -- now authorized")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.get(url, headers=headers2)
process_response(url, r)


# 8) Retrieve list of aliases in a conversation
print("Get Users")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url, headers=headers1)
process_response(url, r)


# 9) Leave a conversation
print("Leave Conversation")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.delete(url, headers=headers2)
process_response(url, r)


# 8) Retrieve list of aliases in a conversation
print("Get Users")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url, headers=headers1)
process_response(url, r)
