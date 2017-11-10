from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE, NOT_AUTH_RESPONSE
import source.framework.constants as c
from source.models.Conversations import Conversations, id_policies
from datetime import datetime
import time


# [BEGIN API python methods]

def get_messages(user, conv_id):
    """Get conversation messages by conversation ID"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_user(user):
            response['messages'] = conv.get_messages()
        else:
            return NOT_AUTH_RESPONSE
    else:
        return NOT_FOUND_RESPONSE
    return response


def create_message(user, conv_id, message_text, media_url):
    """Create a new message"""
    # check user authorization
    # check_user_auth()...
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_user(user):
            # create a new message, add to conv if needed
            message = message_text
            response['messages'] = "Your new message: {}".format(message_text)
        else:
            return NOT_AUTH_RESPONSE
    else:
        return NOT_FOUND_RESPONSE
    return response


def update_message(user, conv_id, message_id):
    """Update (edit) a message"""
    response = {}
    response['messages'] = "Updated message"
    return response


def delete_message(user, conv_id, message_id):
    """Delete a message"""
    response = {}
    response['messages'] = "Deleted message"
    return response

# [END API python methods]


# [BEGIN API handler]

class ConversationMessagesApi(ApiServiceHandler):
    """REST API handler to allow interaction with messages"""

    def get_hook(self, user, *args):
        """Get message API"""
        return get_messages(user, args[0])

    def post_hook(self, user, *args):
        """Create message API"""
        if args[2]:
            return NOT_FOUND_RESPONSE
        return create_message(args[0])

    def put_hook(self, user, *args):
        """Update message API"""
        return update_message(user, args[0], args[1])

    def delete_hook(self, user, *args):
        """Delete message API"""
        return delete_message(user, args[0], args[1])

# [END API handler]
