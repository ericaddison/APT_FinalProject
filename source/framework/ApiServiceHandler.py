from source.framework.BaseHandler import BaseHandler
import source.framework.constants as c
from source.framework.user_authentication import user_authentication

BAD_AUTH_RESPONSE = {'status': 404, 'message': 'User authentication failed'}


class ApiServiceHandler(BaseHandler):
    """Web handler to handle API endpoints"""

    def process(self, method):
        self.set_content_text_json()

        # authenticate user with required access_token
        token = self.get_request_param(c.auth_token_parm)
        user = user_authentication(token)

        # if user not verified or found, return bad response
        if not user:
            response = BAD_AUTH_RESPONSE
        else:
            response = method(user)

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

    def get_hook(self, user):
        return self.notallowed_response('GET')

    def post_hook(self, user):
        return self.notallowed_response('POST')

    def put_hook(self, user):
        return self.notallowed_response('PUT')

    def patch_hook(self, user):
        return self.notallowed_response('PATCH')

    def delete_hook(self, user):
        return self.notallowed_response('DELETE')

    def notallowed_response(self, method):
        return {'message': '{} method not allowed'.format(method), 'status': 405}
