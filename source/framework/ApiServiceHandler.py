from source.framework.BaseHandler import BaseHandler


class ApiServiceHandler(BaseHandler):
    """Web handler to handle API endpoints"""

    def process(self, method):
        self.set_content_text_json()
        response = method()
        if 'status' in response.keys():
            self.response.set_status(response['status'])
        self.write_dictionary_response(response)

    def get(self):
        self.process(self.get_hook)

    def post(self):
        self.process(self.post_hook)

    def put(self):
        self.process(self.put_hook)

    def patch(self):
        self.process(self.patch_hook)

    def delete(self):
        self.process(self.delete_hook)

    def get_hook(self):
        return {'message': 'GET method not allowed', 'status': '405'}

    def post_hook(self):
        return {'message': 'POST method not allowed', 'status': '405'}

    def put_hook(self):
        return {'message': 'PUT method not allowed', 'status': '405'}

    def patch_hook(self):
        return {'message': 'PATCH method not allowed', 'status': '405'}

    def delete_hook(self):
        return {'message': 'DELETE method not allowed', 'status': '405'}

