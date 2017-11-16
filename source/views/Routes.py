from source.framework.webapp2_helpers import make_routes
from source.views.Main import LandingPage
from source.views.Login import LoginPage
from source.views.Manage import ManagePage
from source.views.Create import CreatePage

app = make_routes([
    # [START services]


    # [END services]

    # [START views]
    ('/create', CreatePage),
    ('/manage', ManagePage),
    ('/login', LoginPage),
    ('/.*', LandingPage)
    # [END views]
])
