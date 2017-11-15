import unittest
import source.config.authentication as auth
import requests as req
import json
import random
import time

# For these tests, make sure source.config.authentication has AUTH_PROVIDER set to auth_demo
# Then, token 'DEVTOKEN1' will access dummy user 1
# and token 'DEVTOKEN2' will access dummy user 2

# set up two authorization headers, one for each dummy user
headers1 = {"Authorization": "Bearer DEVTOKEN1"}
headers2 = {"Authorization": "Bearer DEVTOKEN2"}
headers3 = {"Authorization": "Bearer DEVTOKEN3"}


# common setup function
def test_setup(test):
    # create a conversation
    url = 'http://localhost:8080/api/conversations/'
    test.conv_name = "Demo Conversation {}".format(random.randint(0, 10000000))
    r = req.post(url, data={'conv_name': test.conv_name}, headers=headers1)
    test.conv_data = json.loads(r.content)['conversations']
    test.conv_id = test.conv_data['id']
    test.alias1 = test.conv_data['aliases'][0]


class TestLiveApi_Users(unittest.TestCase):
    def setUp(self):
        test_setup(self)

    def test_get_user(self):
        url = 'http://localhost:8080/api/users/'
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'user' in data.keys()
        assert data['user']['email'] == "test@example.com"
        assert data['user']['id'] == 123456789

    def test_update_user(self):
        url = 'http://localhost:8080/api/users/'
        newfname = 'Bob{}'.format(random.randint(0, 100))
        newlname = 'Schubert{}'.format(random.randint(0, 100))
        r = req.put(url, data={'fname': newfname, 'lname': newlname, 'prefcomm': 'web'}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert data['user']['fName'] == newfname
        assert data['user']['lName'] == newlname
        assert data['user']['prefComm'] == 'web'

    def test_delete_user_authorized(self):
        url = 'http://localhost:8080/api/users/'
        r = req.delete(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        print(data)


class TestLiveApi_Conversation(unittest.TestCase):

    def setUp(self):
        test_setup(self)

    def test_create_conversation(self):
        assert self.conv_data['name'] == self.conv_name
        assert len(self.conv_data['aliases']) == 1
        assert self.conv_data['revealOwner']
        assert self.conv_data['viewAfterExpire']

    def test_create_conversation_name_taken(self):
        url = 'http://localhost:8080/api/conversations/'
        r = req.post(url, data={'conv_name': self.conv_name}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 403
        assert data['status'] == 403
        assert 'conversations' in data.keys()
        assert len(data['conversations'].keys()) == 2
        assert data['conversations']['id'] == self.conv_id
        assert data['conversations']['name'] == self.conv_name

    def test_get_conversation_notfound(self):
        url = 'http://localhost:8080/api/conversations/{}'.format(1234)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 404
        assert data['status'] == 404

    def test_get_conversation_unauthorized(self):
        url = 'http://localhost:8080/api/conversations/{}'.format(self.conv_id)
        r = req.get(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'conversations' in data.keys()
        assert len(data['conversations'].keys()) == 2
        assert data['conversations']['id'] == self.conv_id
        assert data['conversations']['name'] == self.conv_name

    def test_get_conversation_authorized(self):
        url = 'http://localhost:8080/api/conversations/{}'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'conversations' in data.keys()
        assert len(data['conversations'].keys()) == 9
        assert data['conversations']['id'] == self.conv_id
        assert data['conversations']['name'] == self.conv_name
        assert data['conversations']['aliases'][0] == self.alias1
        assert data['conversations']['revealOwner']
        assert data['conversations']['viewAfterExpire']


class TestLiveApi_ConvUsers(unittest.TestCase):

    def setUp(self):
        test_setup(self)

    def test_get_aliases_notfound(self):
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(1234)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 404
        assert data['status'] == 404

    def test_get_aliases_unauthorized(self):
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.get(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401
        assert data['status'] == 401

    def test_get_aliases_authorized(self):
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'aliases' in data.keys()
        assert len(data['aliases']) == 1
        assert data['aliases'] == [self.alias1]

    def test_join_conversation_simple(self):
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.post(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'alias' in data.keys()
        assert 'conversation' in data.keys()
        assert len(data['conversation']['aliases']) == 2
        assert data['alias'] in data['conversation']['aliases']
        assert data['conversation']['id'] == self.conv_id

    def test_join_conversation_already_joined(self):
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.post(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'alias' in data.keys()
        assert 'conversation' in data.keys()
        assert len(data['conversation']['aliases']) == 1
        assert data['alias'] in data['conversation']['aliases']
        assert data['conversation']['id'] == self.conv_id

    def test_leave_conversation(self):
        # join conversation
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.post(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert len(data['conversation']['aliases']) == 2
        alias = data['alias']

        # leave conversation
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.delete(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['alias'] == alias
        assert data['conversation']['id'] == self.conv_id
        assert data['conversation']['name'] == self.conv_name

        # make sure conversation down to one user
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert len(data['aliases']) == 1

    def test_join_conversation_leave_join_again(self):
        # join conversation
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.post(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200
        alias = data['alias']

        # leave conversation
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.delete(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200

        # join again, assert same alias
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.post(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['alias'] == alias

    def test_leave_conversation_notjoined(self):
        # leave conversation
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.delete(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401
        assert data['status'] == 401


class TestLiveApi_ConvMessages(unittest.TestCase):

    def setUp(self):
        test_setup(self)

    def test_post_message_notfound(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(1234)
        r = req.post(url, data={"text": "I am a message", "media_url": "http://www.google.com"}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 404
        assert data['status'] == 404

    def test_post_message_unauthorized(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.post(url, data={"text": "I will not work", "media_url": "http://www.failblog.com"}, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401
        assert data['status'] == 401

    def test_post_message_authorized(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        text = "I am a message"
        media_url = "http://www.google.com"
        r = req.post(url, data={"text": text, "media_url": media_url}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'messages' in data.keys()

        msg = data['messages']
        assert msg['convID'] == self.conv_id
        assert msg['convName'] == self.conv_name
        assert not msg['deleted']
        assert msg['text'] == text
        assert msg['mediaURL'] == media_url
        assert msg['userAlias'] == self.alias1

    def test_delete_message_notfound(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(self.conv_id, 1234)
        r = req.delete(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 404
        assert data['status'] == 404

    def test_delete_message_unauthorized(self):
        # post a message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.post(url, data={"text": "lol"}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        msg_id = data['messages']['id']

        # delete the message
        url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(self.conv_id, msg_id)
        r = req.delete(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401
        assert data['status'] == 401

    def test_delete_message_authorized(self):
        # post a message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.post(url, data={"text": "lol"}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        msg_id = data['messages']['id']

        # delete the message
        url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(self.conv_id, msg_id)
        r = req.delete(url, headers=headers1)
        assert r.status_code == 200
        assert data['status'] == 200
        data['messages']['deleted'] == True

    def test_get_messages_notfound(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(1234)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 404
        assert data['status'] == 404

    def test_get_messages_unauthorized(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401
        assert data['status'] == 401

    def test_get_messages_authorized_simple(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200
        assert 'messages' in data.keys()

    def test_edit_message_notfound(self):
        url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(self.conv_id, 1234)
        r = req.put(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 404
        assert data['status'] == 404

    def test_edit_message_notauthorized(self):
        # post a message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        text = "I am a message"
        media_url = "http://www.google.com"
        r = req.post(url, data={"text": text, "media_url": media_url}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        msg_id = data['messages']['id']

        # attempt to edit not authorized
        url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(self.conv_id, msg_id)
        r = req.put(url, data={'text': 'update!'}, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401
        assert data['status'] == 401

    def test_edit_message_authorized(self):
        # post a message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        text = "I am a message"
        media_url = "http://www.google.com"
        r = req.post(url, data={"text": text, "media_url": media_url}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        msg_id = data['messages']['id']

        # attempt to edit not authorized
        url = 'http://localhost:8080/api/conversations/{}/messages/{}'.format(self.conv_id, msg_id)
        newtext = 'update!'
        newmedia = 'www.new.com'
        r = req.put(url, data={'text': newtext, 'media_url': newmedia}, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200

        # get the messages
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        assert r.status_code == 200
        assert data['status'] == 200

        msg = data['messages'][0]
        assert msg['text'] == newtext
        assert msg['mediaURL'] == newmedia
        assert len(msg['edits']) == 2

    def test_post_message_authorized_msgcount_onemessage(self):
        # get messages and record message count
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        msg_count = len(data['messages'])
        assert msg_count == 0

        # post new message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        text = "I am a message"
        media_url = "http://www.google.com"
        r = req.post(url, data={"text": text, "media_url": media_url}, headers=headers1)
        assert r.status_code == 200

        # get messages again
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        msg_count = len(data['messages'])
        assert msg_count == 1
        assert data['messages'][0]['text'] == text
        assert data['messages'][0]['mediaURL'] == media_url

    def test_post_message_authorized_msgcount_twomessages(self):
        # get messages and record message count
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        msg_count = len(data['messages'])
        assert msg_count == 0

        # post new message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        text = "I am a message"
        media_url = "http://www.google.com"
        r = req.post(url, data={"text": text, "media_url": media_url}, headers=headers1)
        assert r.status_code == 200

        # post new message again
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        text2 = "I am another message"
        media_url2 = "http://www.googleeee.com"
        r = req.post(url, data={"text": text2, "media_url": media_url2}, headers=headers1)
        assert r.status_code == 200

        # get messages again
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.get(url, headers=headers1)
        data = json.loads(r.content)
        msg_count = len(data['messages'])
        assert msg_count == 2
        assert data['messages'][0]['text'] == text
        assert data['messages'][0]['mediaURL'] == media_url
        assert data['messages'][1]['text'] == text2
        assert data['messages'][1]['mediaURL'] == media_url2

    def test_join_conversation_and_post_message(self):
        # try to post message
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.post(url, data={"text": "I will not work", "media_url": "http://www.failblog.com"}, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 401

        # join conversation
        url = 'http://localhost:8080/api/conversations/{}/users/'.format(self.conv_id)
        r = req.post(url, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200

        # try to post message again
        url = 'http://localhost:8080/api/conversations/{}/messages/'.format(self.conv_id)
        r = req.post(url, data={"text": "I should work", "media_url": "http://www.victory.com"}, headers=headers2)
        data = json.loads(r.content)
        assert r.status_code == 200


if __name__ == '__main__':
    unittest.main()