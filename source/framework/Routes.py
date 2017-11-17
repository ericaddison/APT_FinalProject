from source.framework.webapp2_helpers import make_routes
from source.framework.MailHandlers import ConversationMailHandler, GeneralMailHandler
import webapp2

app = webapp2.WSGIApplication(
    routes=[
        ('/_ah/mail/conversation_\d+@sg\.hailing-frequencies-2017\.appspotmail\.com', ConversationMailHandler),
        ('/_ah/mail/.*', GeneralMailHandler)
    ], debug=True)
