from source.framework.BaseHandler import BaseHandler
from source.framework.user_authentication import user_authentication

BAD_AUTH_RESPONSE = {'status': 404, 'message': 'User authentication failed'}
NOT_AUTH_RESPONSE = {'status': 401, 'message': 'Not authorized'}
NOT_FOUND_RESPONSE = {'message': 'Wah wah, not found ;)', 'status': 404}


class ApiServiceHandler(BaseHandler):
    """Web handler to handle API endpoints"""

    def process(self, method, *args):
        self.set_content_text_json()

        # dummy user for debug
        #user = Users.dummy_user()

        # authenticate user with required access_token
        user = None
        auth_header = self.get_auth_header()
        if auth_header:
           user = user_authentication(auth_header)
        else:
           print("ApiServiceHandler.process(): no auth_header found")

        # if user not verified or found, return bad response
        if not user:
            response = BAD_AUTH_RESPONSE
        else:
            response = method(user, *args)

        if 'status' in response.keys():
            self.response.set_status(response['status'])

        self.write_dictionary_response(response)

    def get(self, *args):
        self.process(self.get_hook, *args)

    def post(self, *args):
        self.process(self.post_hook, *args)

    def put(self, *args):
        self.process(self.put_hook, *args)

    def delete(self, *args):
        self.process(self.delete_hook, *args)

    def get_hook(self, user, *args):
        return self.notallowed_response('GET')

    def post_hook(self, user, *args):
        return self.notallowed_response('POST')

    def put_hook(self, user, *args):
        return self.notallowed_response('PUT')

    def delete_hook(self, user, *args):
        return self.notallowed_response('DELETE')

    def notallowed_response(self, method):
        return {'message': '{} method not allowed'.format(method), 'status': 405}
