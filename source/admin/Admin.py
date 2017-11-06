from source.framework.BaseHandler import BaseHandler


class AdminDashboard(BaseHandler):
    """Admin dashboard to allow admin and testing access"""
    def get(self):

        template_values = {}
        self.render_template('admin/AdminDashboard.html', template_values)
