import webapp2

from source.Main import ManagePage

app = webapp2.WSGIApplication([

    # [START views]
    ('/manage', ManagePage)
    # [END views]

], debug=True)
