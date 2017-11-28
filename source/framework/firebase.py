import requests as req
import json
# interact with the Firebase DB

base_url = 'https://hailing-frequencies-2017.firebaseio.com/messages'


def post_message_to_firebase(convmsg, token):
    convID = convmsg.get_conversation_id()

    payload = {'name': convmsg.alias, 'photoUrl': convmsg.get_media_url(), 'text': convmsg.get_text()}

    req.post('{0}/{1}.json?auth = {2}'.format(base_url, convID, token), data=json.dumps(payload))