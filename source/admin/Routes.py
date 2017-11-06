from source.framework.webapp2_helpers import make_routes
from source.admin.Admin import AdminDashboard

app = make_routes([
    ('/admin/', AdminDashboard)
])
