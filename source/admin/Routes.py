import webapp2

app = webapp2.WSGIApplication([

    # [START views]
    ('/admin/', ManagePage)
    # [END views]

], debug=True)
