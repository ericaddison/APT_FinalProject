from source.framework.BaseHandler import BaseHandler



class ViewPage(BaseHandler):
    def get(self):
        template_values = {}



        self.render_template('app/ViewPage.html', template_values)
