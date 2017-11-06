from source.framework.BaseHandler import BaseHandler


class AdminDashboard(BaseHandler):
    def get(self):

        template_values = {}
        self.render_template('templates/admin/AdminDashboard.html', template_values)
