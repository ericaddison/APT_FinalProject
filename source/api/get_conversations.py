from source.framework.BaseHandler import BaseHandler


def get_conversations(names=None):
    """Get conversations by name, or get all conversations if no names provided"""
    if names is None:
        return "All conversations"
    else:
        return "Requested conversations"


class GetConversations(BaseHandler):
    """API handler to allow getting conversation data"""
    def get(self):
        self.set_content_text_json()
        response = {}

        response['conversations'] = get_conversations()
        self.write_dictionary_response(response)
