from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE, NOT_AUTH_RESPONSE
from source.models.Conversations import Conversations
from source.models.ConvUsers import ConvUsers


# [BEGIN API python methods]

def get_convusers(user, conv_id):
    """Get conversation users by conversation ID"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_user(user):
            response['aliases'] = conv.get_aliases()
        else:
            return NOT_AUTH_RESPONSE
    else:
        return NOT_FOUND_RESPONSE
    return response


def create_message(user, conv_id, text, media_url):
    """Create a new message"""
    # check user authorization
    # check_user_auth()...
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_user(user):
            user_alias = "Mr. Black"
            msg = ConvMessages.create(user, user_alias, conv, text, media_url)
            conv.put_message(msg)
            response['messages'] = msg.get_full_data()
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

class ConvUsersApi(ApiServiceHandler):
    """REST API handler to allow interaction with ConvUsers"""

    def get_hook(self, user, *args):
        """Get ConvUsers API"""
        return get_convusers(user, args[0])

    def post_hook(self, user, *args):
        """Create ConvUser (user join conversation) API"""
        if args[1]:
            return NOT_FOUND_RESPONSE
        return create_convuser(user, args[0], "hello", "")

    def delete_hook(self, user, *args):
        """Delete convUser (user leave conversation) API"""
        return delete_convuser(user, args[0], args[1])

# [END API handler]
