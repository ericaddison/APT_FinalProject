from source.framework.BaseHandler import BaseHandler



class ProfilePage(BaseHandler):
    def get(self):
        template_values = {}

        self.render_template('app/ProfilePage.html', template_values)

