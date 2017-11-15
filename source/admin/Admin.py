from source.framework.BaseHandler import BaseHandler


class AdminLanding(BaseHandler):
    """Admin dashboard to allow admin and testing access"""
    def get(self):

        template_values = {'html_template': 'admin/AdminTemplate.html'}
        self.render_template('admin/AdminLanding.html', template_values)


class AdminConversations(BaseHandler):
    """Admin dashboard to allow admin and testing access"""
    def get(self):

        template_values = {'html_template': 'admin/AdminTemplate.html'}
        self.render_template('admin/AdminConversations.html', template_values)

class AdminUsers(BaseHandler):
    """Admin dashboard to allow admin and testing access"""
    def get(self):

        template_values = {'html_template': 'admin/AdminTemplate.html'}
        self.render_template('admin/AdminUsers.html', template_values)

class AdminMessages(BaseHandler):
    """Admin dashboard to allow admin and testing access"""
    def get(self):

        template_values = {'html_template': 'admin/AdminTemplate.html'}
        self.render_template('admin/AdminMessages.html', template_values)
