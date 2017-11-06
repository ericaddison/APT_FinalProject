from source.framework.webapp2_helpers import make_routes
from source.views.Main import LandingPage

app = make_routes([
    # [START views]
    ('/.*', LandingPage)
    # [END views]
])
