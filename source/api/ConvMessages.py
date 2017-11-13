from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE, NOT_AUTH_RESPONSE
from source.models.Conversations import Conversations
from source.models.ConvMessages import ConvMessages
import source.framework.constants as c
from source.framework.communicate import broadcast_message
from source.api.api_helpers import process_apicall_checkconv_checkuser, process_apicall_checkconv

# [BEGIN API python methods]

def get_messages(user, conv_id):
    """Get conversation messages by conversation ID"""

    def get_messages(user, conv, response):
        response['messages'] = conv.get_messages_full_data()
        return response

    return process_apicall_checkconv_checkuser(user, conv_id, get_messages)


def create_message(user, conv_id, text, media_url):
    """Create a new message"""

    def create_message(user, conv, response):
        user_alias = conv.get_alias_for_user(user)
        msg = ConvMessages.create(user, user_alias, conv, text, media_url)
        conv.put_message(msg)
        # send new msg to all users in this conv
        broadcast_message(msg)
        response['messages'] = msg.get_full_data()
        return response

    return process_apicall_checkconv_checkuser(user, conv_id, create_message)


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

class ConvMessagesApi(ApiServiceHandler):
    """REST API handler to allow interaction with messages"""

    def get_hook(self, user, *args):
        """Get message API"""
        return get_messages(user, args[0])

    def post_hook(self, user, *args):
        """Create message API"""
        if args[1]:
            return NOT_FOUND_RESPONSE
        text = self.get_request_param(c.text_param)
        media_url = self.get_request_param(c.media_url_param)
        return create_message(user, args[0], text, media_url)

    def put_hook(self, user, *args):
        """Update message API"""
        return update_message(user, args[0], args[1])

    def delete_hook(self, user, *args):
        """Delete message API"""
        return delete_message(user, args[0], args[1])

# [END API handler]
