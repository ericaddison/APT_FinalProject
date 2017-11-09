from source.framework.ApiServiceHandler import ApiServiceHandler


# [BEGIN API python methods]

def get_conversations(user, conv_id):
    """Get conversations by name, or get all conversations if no names provided"""
    response = {}
    if conv_id == "":
        response['conversations'] = "All conversations"
    else:
        response['conversations'] = "Requested conversations: {}".format(conv_id)
    return response


def create_conversation(user, conv_id):
    """Create a new conversation"""
    response = {}
    response['conversations'] = "New conversation"
    return response


def update_conversation(user, conv_id):
    """Update conversation settings"""
    response = {}
    response['conversations'] = "Updated conversation"
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

    def get_hook(self, user, url_id):
        """Get conversation data API"""
        return get_conversations(user, url_id)

    def post_hook(self, user, url_id):
        """Create conversation data API"""
        return create_conversation(user)

    def put_hook(self, user, url_id):
        """Update conversation API"""
        return update_conversation(user, url_id)

    def delete_hook(self, user, url_id):
        """Delete conversation API"""
        return delete_conversation(user, url_id)

# [END API handler]
