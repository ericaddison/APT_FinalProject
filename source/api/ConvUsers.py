from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE
from source.api.api_helpers import process_apicall_checkconv_checkuser, process_apicall_checkconv
import source.framework.constants as c


# [BEGIN API python methods]

def get_convusers(user, conv_id):
    """Get conversation users by conversation ID"""

    # method to call if user is part of the conversation
    def get_aliases(user, conv, response):
        response['aliases'] = conv.get_active_aliases()
        return response

    return process_apicall_checkconv_checkuser(user, conv_id, get_aliases)


def create_convuser(user, conv_id, comm_option, comm_detail):
    """Create a new convuser (user join conversation)"""

    # method to call if valid conversation
    def join_conv(user, conv, response):
        cuser = conv.add_user(user, comm_option, comm_detail)
        response['alias'] = cuser
        response['conversation'] = conv.get_full_data()
        return response

    return process_apicall_checkconv(user, conv_id, join_conv)


def delete_convuser(user, conv_id):
    """Delete a convuser (user leave a conversation)"""

    # method to call if user is part of the conversation
    def remove_user(user, conv, response):
        cuser = conv.remove_user(user)
        if cuser:
            response['alias'] = cuser
        else:
            return NOT_FOUND_RESPONSE
        response['conversation'] = conv.get_basic_data()
        return response

    return process_apicall_checkconv_checkuser(user, conv_id, remove_user)


# [END API python methods]


# [BEGIN API handler]

class ConvUsersApi(ApiServiceHandler):
    """REST API handler to allow interaction with ConvUsers"""

    def get_hook(self, user, *args, **kwargs):
        """Get ConvUsers API"""
        return get_convusers(user, args[0])

    def post_hook(self, user, *args, **kwargs):
        """Create ConvUser (user join conversation) API"""
        if args[1]:
            return NOT_FOUND_RESPONSE

        comm_option = self.get_request_param(c.commoption_parm)
        comm_detail = self.get_request_param(c.commdetail_parm)

        return create_convuser(user, args[0], comm_option, comm_detail)

    def delete_hook(self, user, *args, **kwargs):
        """Delete convUser (user leave conversation) API"""
        return delete_convuser(user, args[0])

# [END API handler]
