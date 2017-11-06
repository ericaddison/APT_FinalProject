from source.framework.ApiServiceHandler import ApiServiceHandler


def get_conversations(names=None):
    """Get conversations by name, or get all conversations if no names provided"""
    response = {}
    if names is None:
        response['conversations'] = "All conversations"
    else:
        response['conversations'] = "Requested conversations"
    return response


def create_conversation():
    """Create a new conversation"""
    response = {}
    response['conversations'] = "New conversations"
    return response


class ConversationsApi(ApiServiceHandler):
    """REST API handler to allow interaction with conversation data"""

    def get_hook(self):
        """Get conversation data API"""
        return get_conversations()

    def post_hook(self):
        """Set conversation data API"""
        return create_conversation()