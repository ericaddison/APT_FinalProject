import requests as req
import json
from pprint import pprint


# demos of calling the web API
#
# What should we be able to do?
# 1) create a conversation (GOOD)
# 2) retrieve conversation details (GOOD)
# 3) Delete a conversation (?)
# 4) Post a message to a conversation (GOOD)
# 5) Retrieve messages from a conversation (GOOD)
# 6) Edit a message in a conversation
# 7) Delete a message in a conversation
# 8) Retrieve list of aliases in a conversation (GOOD)
# 9) Leave a conversation (GOOD)
# 10) Join an existing conversation (GOOD)


def process_response(url, r):
    rdict = json.loads(r.content)
    print("Response from {}".format(url))
    pprint(rdict)
    print("\n")
    return rdict

# 1) create a conversation
print("Create Conversation")
url = 'http://localhost:8080/api/conversations/'
r = req.post(url, data={"conv_name": "Demo Conversation"})
print(r)
r0 = process_response(url, r)
conv_id = r0['conversations']['id']

# 2) retrieve conversation details
print("Get Conversation Info")
url = 'http://localhost:8080/api/conversations/{}'.format(conv_id)
r = req.get(url)
process_response(url, r)

# 8) Retrieve list of aliases in a conversation
print("Get Users")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url)
process_response(url, r)

# 4) Post a message to a conversation
print("Post Message")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.post(url, data={"text": "I am a message", "media_url": "http://www.google.com"})
process_response(url, r)

# 5) Retrieve messages from a conversation
print("Get Messages")
url = 'http://localhost:8080/api/conversations/{}/messages/'.format(conv_id)
r = req.get(url)
process_response(url, r)

# 9) Leave a conversation
print("Leave Conversation")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.delete(url)
process_response(url, r)

# 8) Retrieve list of aliases in a conversation
print("Get Users")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url)
process_response(url, r)

# 10) Join an existing conversation
print("Join Conversation")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.post(url)
process_response(url, r)

# 8) Retrieve list of aliases in a conversation
print("Get Users")
url = 'http://localhost:8080/api/conversations/{}/users/'.format(conv_id)
r = req.get(url)
process_response(url, r)