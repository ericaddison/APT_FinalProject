from source.framework.webapp2_helpers import make_routes
from source.views.Main import LandingPage
from auth0_demo import Auth0LoginCallback, Auth0MainPage
from source.views.Login import LoginPage
from source.views.Manage import ManagePage
from source.views.Create import CreatePage

app = make_routes([
    # [START auth0 demo]
    ('/auth0demo/', Auth0MainPage),
    ('/auth0demo/callback', Auth0LoginCallback),
    # [END auth0 demo]

    # [START services]


    # [END services]

    # [START views]
    ('/create', CreatePage),
    ('/manage', ManagePage),
    ('/login', LoginPage),
    ('/.*', LandingPage)
    # [END views]
])
