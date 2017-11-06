from source.framework.BaseHandler import BaseHandler


class ApiServiceHandler(BaseHandler):
    """Web handler to handle API endpoints"""

    def write_response(self, response):
        if 'status' in response.keys():
            self.response.set_status(response['status'])
        self.write_dictionary_response(response)

    def get(self):
        self.set_content_text_json()
        response = self.get_hook()
        self.write_response(response)

    def post(self):
        self.set_content_text_json()
        response = self.post_hook()
        self.write_response(response)

    def put(self):
        self.set_content_text_json()
        response = self.put_hook()
        self.write_response(response)

    def patch(self):
        self.set_content_text_json()
        response = self.patch_hook()
        self.write_response(response)

    def delete(self):
        self.set_content_text_json()
        response = self.delete_hook()
        self.write_response(response)


