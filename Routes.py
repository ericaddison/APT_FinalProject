import webapp2

from source.services.Service_Management import ManagementService
from source.views.ErrorView import ErrorView
from source.Main import ManagePage

config = {'webapp2_extras.sessions': {'secret_key': 'my-super-secret-key'}}

app = webapp2.WSGIApplication([

    # [START views]
    ('/manage', ManagePage)
    # [END views]

    # [START services]
    ('/services/management', ManagementService)
    # [END services]

], config=config, debug=True)
