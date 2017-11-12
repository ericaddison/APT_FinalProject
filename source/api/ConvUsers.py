from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE, NOT_AUTH_RESPONSE
from source.models.Conversations import Conversations
from source.models.ConvUsers import ConvUsers


# [BEGIN API python methods]

def get_convusers(user, conv_id):
    """Get conversation users by conversation ID"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_active_user(user):
            response['aliases'] = conv.get_active_aliases()
        else:
            return NOT_AUTH_RESPONSE
    else:
        return NOT_FOUND_RESPONSE
    return response


def create_convuser(user, conv_id):
    """Create a new convuser (user join conversation)"""
    # check user authorization
    # check_user_auth()...
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        cuser = conv.add_user(user)
        response['alias'] = cuser.displayName
        response['conversation'] = conv.get_full_data()
    else:
        return NOT_FOUND_RESPONSE
    return response


def delete_convuser(user, conv_id):
    """Delete a convuser (user leave a conversation)"""
    # check user authorization
    # check_user_auth()...
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_active_user(user):
            cuser = conv.remove_user(user)
            if cuser:
                response['alias'] = cuser.displayName
            else:
                return NOT_FOUND_RESPONSE
            response['conversation'] = conv.get_basic_data()
        else:
            return NOT_AUTH_RESPONSE
    else:
        return NOT_FOUND_RESPONSE
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
        return create_convuser(user, args[0])

    def delete_hook(self, user, *args):
        """Delete convUser (user leave conversation) API"""
        return delete_convuser(user, args[0])

# [END API handler]
