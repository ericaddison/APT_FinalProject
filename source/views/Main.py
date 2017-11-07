from source.framework.BaseHandler import BaseHandler


class LandingPage(BaseHandler):
    """The home page"""
    def get(self):

        template_values = {}
        self.render_template('app/LandingPage.html', template_values)

class LoginPage(BaseHandler):
    def get(self):
        template_values = {}
        self.render_template('app/LoginPage.html', template_values)


