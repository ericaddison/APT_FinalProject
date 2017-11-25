import logging
from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE
from source.config.defaults import DEFAULT_CONVERSATION_LIFETIME_SECONDS
import source.framework.constants as c
from source.models.Conversations import Conversations, id_policies
from datetime import datetime
from dateutil import parser
import time
from source.api.api_helpers import process_apicall_checkconv_checkuser

# [BEGIN API python methods]


def get_conversations(user, conv_id):
    """Get conversations by name, or get all conversations if no names provided"""
    logging.debug("***get_conversations")

    # method to call if user is part of the conversation
    def full_data(user, conv, response):
        response['conversations'] = conv.get_full_data()
        return response

    def basic_data(user, conv, response):
        response['conversations'] = conv.get_basic_data()
        return response

    if conv_id == "":
        response = {'status': 200}
        response['conversations'] = Conversations.get_all_active_conversations_basic_data()
    else:
        response = process_apicall_checkconv_checkuser(user, conv_id, full_data, basic_data)

    return response


def create_conversation(user, name, destroy_date, id_policy, view_after_expire, reveal_owner, restrict_comms, password_hash):
    """Create a new conversation"""

    # default values
    name = name if name else Conversations.random_name()
    id_policy = id_policy if id_policy in id_policies else "colors"

    three_months = datetime.fromtimestamp(time.time()+DEFAULT_CONVERSATION_LIFETIME_SECONDS)
    destroy_date = parser.parse(destroy_date) if destroy_date else three_months
    destroy_date = destroy_date if destroy_date > datetime.now() else three_months

    view_after_expire = False if view_after_expire.lower() == 'false' else True
    reveal_owner = False if reveal_owner.lower() == 'false' else True
    restrict_comms = restrict_comms if restrict_comms else ""
    password_hash = password_hash if password_hash else ""

    status, conv = Conversations.create(name=name,
                                        owner=user,
                                        destroy_date=destroy_date,
                                        id_policy=id_policy,
                                        view_after_expire=view_after_expire,
                                        reveal_owner=reveal_owner,
                                        restrict_comms=restrict_comms,
                                        password_hash=password_hash)

    if status:
        return {'conversations': conv.get_full_data(), 'status': 200}
    else:
        return {'message': 'Conversation name already taken',
                'conversations': conv.get_basic_data(),
                'status': 403}


def update_conversation(user, conv_id, name, destroy_date,
                        id_policy, view_after_expire, reveal_owner,
                        restrict_comms, password):
    """Update conversation settings"""
    response = {}
    thisConvo =  Conversations.get_conversation_by_id(conv_id)
    print "user: ", user
    print "owner: ", thisConvo.owner.get()
    if user is thisConvo.owner.get():
        thisConvo.name = name
        thisConvo.destroyDate = datetime.strptime(destroy_date, '%Y-%m-%d')
        thisConvo.idPolicy = id_policy
        thisConvo.viewAfterExpire = (view_after_expire == 'true')
        thisConvo.revealOwner = (reveal_owner == 'true')
        thisConvo.restrictComms = restrict_comms
        thisConvo.password = password
        thisConvo.put()
        response['conversations'] = "Updated conversation"
    else:
        response['conversations'] = "You are not the owner"
    return response


def delete_conversation(user, conv_id):
    """Delete a conversation"""
    response = {}
    response['conversations'] = "Deleted conversation"
    return response

# [END API python methods]


# [BEGIN API handler]

class ConversationsApi(ApiServiceHandler):
    """REST API handler to allow interaction with conversation data"""

    def get_hook(self, user, *args):
        """Get conversation data API"""
        return get_conversations(user, args[0])

    def post_hook(self, user, *args):
        """Create conversation data API"""
        logging.debug("***post_hook user: {}, args: {}".format(user, args))
        if args[0]:
            return NOT_FOUND_RESPONSE

        # dummy version, for now
        name = self.get_request_param(c.conversastion_name_parm)
        destroy_date = self.get_request_param(c.destroydate_parm)
        id_policy = self.get_request_param(c.idpolicy_parm)
        view_after_expire = self.get_request_param(c.view_after_expire_parm)
        reveal_owner = self.get_request_param(c.reveal_owner_parm)
        restrict_comms = self.get_request_param(c.restrict_comms_parm)
        password = self.get_request_param(c.password_parm)

        return create_conversation(user, name,
                                   destroy_date, id_policy,
                                   view_after_expire, reveal_owner,
                                   restrict_comms, password)

    def put_hook(self, user, *args):
        """Update conversation API"""
        name = self.get_request_param(c.conversastion_name_parm)
        destroy_date = self.get_request_param(c.destroydate_parm)
        id_policy = self.get_request_param(c.idpolicy_parm)
        view_after_expire = self.get_request_param(c.view_after_expire_parm)
        reveal_owner = self.get_request_param(c.reveal_owner_parm)
        restrict_comms = self.get_request_param(c.restrict_comms_parm)
        password = self.get_request_param(c.password_parm)
        print"***update name: ", name
        return update_conversation(user, args[0], name, destroy_date,
                                   id_policy, view_after_expire, reveal_owner,
                                   restrict_comms, password)

    def delete_hook(self, user, *args):
        """Delete conversation API"""
        return delete_conversation(user, args[0])






class OwnedConversationsApi(ApiServiceHandler):
        """REST API handler to allow interaction with conversation data"""

        def get_hook(self, user, *args):
            """Get conversation data API"""
            return get_my_conversations(user)


def get_my_conversations(user):
    """Get conversations by name, or get all conversations if no names provided"""
    logging.debug("***get_my_conversations")
    response = {'status': 200}
    results = Conversations.get_conversation_by_owner(user)
    convList = []
    for conv in results:
        convList.append({'id': conv.key.id(), 'name': conv.name})

    response['conversations'] = convList

    return response