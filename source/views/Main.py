from source.framework.BaseHandler import BaseHandler


class LandingPage(BaseHandler):
    def get(self):

        template_values = {}
        self.render_template('templates/app/LandingPage.html', template_values)



