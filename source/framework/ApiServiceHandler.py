from source.framework.BaseHandler import BaseHandler

NO_USER_RESPONSE = {'status': 404, 'message': 'User not found'}


class ApiServiceHandler(BaseHandler):
    """Web handler to handle API endpoints"""

    def process(self, method):
        self.set_content_text_json()

        # authenticate user here #
        user = None
        if not user:
            response = NO_USER_RESPONSE
        else:
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
        return self.notallowed_response('GET')

    def post_hook(self):
        return self.notallowed_response('POST')

    def put_hook(self):
        return self.notallowed_response('PUT')

    def patch_hook(self):
        return self.notallowed_response('PATCH')

    def delete_hook(self):
        return self.notallowed_response('DELETE')

    def notallowed_response(self, method):
        return {'message': '{} method not allowed'.format(method), 'status': '405'}
