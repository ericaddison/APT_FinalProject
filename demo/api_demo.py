import requests as req
import json
# demos of calling the web API


# make a new conversation
r = req.post('http://localhost:8080/api/conversations/')
conv_id = json.loads(r.content)['conversations']['id']
print('Created new conversation with id {}'.format(conv_id))

# retrieve that conversation
r = req.get('http://localhost:8080/api/conversations/{}'.format(conv_id))
print('Retrieved conversation: {}'.format(r.content))

# get the users from that conversation
r = req.get('http://localhost:8080/api/conversations/{}/users/'.format(conv_id))
print('Retrieved conversation: {}'.format(r.content))
