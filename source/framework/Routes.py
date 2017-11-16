from source.framework.webapp2_helpers import make_routes
from source.framework.MailHandler import MailHandler
import webapp2

app = webapp2.WSGIApplication(routes=[MailHandler.mapping()], debug=True)
