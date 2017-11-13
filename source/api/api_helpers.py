from source.models.Conversations import Conversations
from source.framework.ApiServiceHandler import NOT_FOUND_RESPONSE, NOT_AUTH_RESPONSE


def default_no_user(user, conv, response):
    return NOT_AUTH_RESPONSE


def default_no_conv(user, conv, response):
    return NOT_FOUND_RESPONSE


def process_apicall_checkconv_checkuser(user, conv_id, has_user_method,
                                        no_user_method=default_no_user,
                                        no_conv_method=default_no_conv):
    """Process a request that requires checking valid conversation and that the user is part of the conversation"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        if conv.has_active_user(user):
            response = has_user_method(user, conv, response)
        else:
            print("returning: {}".format(no_user_method(user, conv, response)))
            response = no_user_method(user, conv, response)
    else:
        response = no_conv_method(user, conv, response)
    return response


def process_apicall_checkconv(user, conv_id, valid_conv_method):
    """Process a request that requires checking valid conversation only"""
    response = {'status': 200}
    conv = Conversations.get_conversation_by_id(conv_id)
    if conv:
        valid_conv_method(user, conv, response)
    else:
        return NOT_FOUND_RESPONSE
    return response