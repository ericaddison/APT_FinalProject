from source.framework.webapp2_helpers import make_routes
import source.admin.Admin as Admin

app = make_routes([
    ('/admin/', Admin.AdminLanding),
    ('/admin/conversations/', Admin.AdminConversations),
    ('/admin/messages/', Admin.AdminMessages),
    ('/admin/users/', Admin.AdminUsers)
])
