from source.framework.webapp2_helpers import make_routes
from source.views.Main import LandingPage
from source.views.Login import LoginPage
from source.views.Profile import ProfilePage
from source.views.Manage import ManagePage
from source.views.Manage import ManageConvoPage
from source.views.Create import CreatePage
from source.views.View import ViewPage

app = make_routes([
    # [START services]


    # [END services]

    # [START views]
    ('/view/.*', ViewPage),
    ('/create', CreatePage),
    ('/profile', ProfilePage),
    ('/manage', ManagePage),
    ('/manage/.*', ManageConvoPage),
    ('/login', LoginPage),
    ('/.*', LandingPage)
    # [END views]
])
