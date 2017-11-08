from source.framework.BaseHandler import BaseHandler
import json


class ApiTestAuth(BaseHandler):
    def get(self):
        self.render_template('app/test/API_test.html', {})


class ApiTestCallback(BaseHandler):
    def get(self):

        # if we are here, it came from API_test.html!!!

        # send it back to another test page to display

        code = self.get_request_param('code')

        template_values = {'authcode': code}
        self.render_template('app/test/API_callback.html', template_values)
