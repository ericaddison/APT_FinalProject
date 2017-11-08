from source.framework.ApiServiceHandler import ApiServiceHandler
from source.models.ConvMessages import ConvMessages
import source.framework.constants as c


# I think these endpoints should show up more like
# /conversations/<conv id>/messages/

def get_messages(conv_id):
    """Get all messages for a given conversation"""
    # this should be a class method
    # make the date field sortable (how did we do that?)
    ConvMessages.get_messages_by_conversation(conv_id)

    # format each message as a dictionary (probably put this convenience in class)
    # like to hold { 'text': '...', 'media_url':'...', 'owner': '...', 'date': '...', 'id': '...'}
    # then send back the message id for other operations, like edit or delete
    # probably also want a field in ConvMessage class to hold alias (obfuscated user name)

    response = {}
    response['messages'] = "All messages for conversation"
    return response


def create_message(conv_id, text, user, media_url=''):
    """Post a new message to a conversation"""

    response = {}
    response['messages'] = "New message"
    return response


def edit_message():
    """Edit an existing message"""
    response = {}
    response['messages'] = "Updated message"
    return response


def delete_message():
    """Delete a message from a conversation"""
    response = {}
    response['messages'] = "Deleted message"
    return response


class MessagesApi(ApiServiceHandler):
    """REST API handler to allow interaction with message data"""

    def get_hook(self, user):
        """Get messages API"""
        conv_id = self.get_request_param(c.conversastion_id_parm)
        return get_messages(conv_id)

    def post_hook(self, user):
        """Create message API"""
        conv_id = self.get_request_param(c.conversastion_id_parm)
        return create_message(conv_id)

    def put_hook(self, user):
        """Update message API"""
        conv_id = self.get_request_param(c.conversastion_id_parm)
        return edit_message(conv_id)

    def delete_hook(self, user):
        """Delete message API"""
        conv_id = self.get_request_param(c.conversastion_id_parm)
        return delete_message(conv_id)
