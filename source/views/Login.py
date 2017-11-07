from source.framework.BaseHandler import BaseHandler


class LoginPage(BaseHandler):
    def post(self):
        template_values = {}
        email = self.get_request_param('email')
        fname = self.get_request_param('fname')
        lname = self.get_request_param('lname')
        self.render_template('app/LandingPage.html', template_values)


    def get(self):
        template_values = {}
        self.render_template('app/LoginPage.html', template_values)