import webapp2

from source.services.Service_Management import ManagementService
from source.Main import ManagePage

app = webapp2.WSGIApplication([

    # [START services]
    ('/services/management', ManagementService)
    # [END services]

], config=config, debug=True)
