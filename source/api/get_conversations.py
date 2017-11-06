from source.framework.BaseHandler import BaseHandler


class GetConversations(BaseHandler):
    def get(self):
        self.set_content_text_json()
        response = {}

        response['message'] = "GetConversations() Not implemented yet"
        self.write_dictionary_response(response)
