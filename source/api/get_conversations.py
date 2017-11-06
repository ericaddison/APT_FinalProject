def get_conversations(names=None):
    """Get conversations by name, or get all conversations if no names provided"""
    if names is None:
        return "All conversations"
    else:
        return "Requested conversations"


from source.framework.BaseHandler import BaseHandler


class GetConversations(BaseHandler):
    def get(self):
        self.set_content_text_json()
        response = {}

        response['conversations'] = get_conversations()
        self.write_dictionary_response(response)
