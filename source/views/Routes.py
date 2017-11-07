from source.framework.webapp2_helpers import make_routes
from source.views.Main import LandingPage
from auth0_demo import Auth0LoginCallback, Auth0MainPage
from source.views.Login import LoginPage

app = make_routes([
    # [START auth0 demo]
    ('/auth0demo/', Auth0MainPage),
    ('/auth0demo/callback', Auth0LoginCallback),
    # [END auth0 demo]

    # [START views]
    ('/login', LoginPage),
    ('/.*', LandingPage)
    # [END views]
])
