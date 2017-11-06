from source.framework.BaseHandler import BaseHandler


def get_conversations(names=None):
    """Get conversations by name, or get all conversations if no names provided"""
    response = {}
    if names is None:
        response['conversations'] = "All conversations"
    else:
        response['conversations'] = "Requested conversations"
    return response


class GetConversations(BaseHandler):
    """API handler to allow getting conversation data"""
    def get(self):
        self.set_content_text_json()
        response = get_conversations()
        self.write_dictionary_response(response)
