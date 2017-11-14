from source.framework.BaseHandler import BaseHandler


class AdminDashboard(BaseHandler):
    """Admin dashboard to allow admin and testing access"""
    def get(self):

        template_values = {'html_template': 'admin/AdminTemplate.html'}
        self.render_template('admin/AdminDashboard.html', template_values)
