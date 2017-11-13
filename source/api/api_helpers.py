from source.models.Conversations import Conversations
from source.framework.ApiServiceHandler import NOT_FOUND_RESPONSE, NOT_AUTH_RESPONSE


def process_request_checkconv_checkuser(user, conv_id, has_user_method):
    """Process a request that requires checking valid conversation and that the user is part of the conversation"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_active_user(user):
            has_user_method(user, conv, response)
        else:
            return NOT_AUTH_RESPONSE
    else:
        return NOT_FOUND_RESPONSE
    return response


def process_request_checkconv(user, conv_id, valid_conv_method):
    """Process a request that requires checking valid conversation only"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        valid_conv_method(user, conv, response)
    else:
        return NOT_FOUND_RESPONSE
    return response