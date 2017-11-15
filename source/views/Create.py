from source.framework.BaseHandler import BaseHandler



class CreatePage(BaseHandler):
    def get(self):
        template_values = {}

        self.render_template('app/CreatePage.html', template_values)
