from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import logging


class MailHandler(InboundMailHandler):
    """Web handler to incoming emails"""

    def receive(self, email):
        logging.info("Received a message from: " + email.sender)
        logging.info("subject: " + email.subject)
        logging.info("to: " + email.to)

        if hasattr(email, 'cc'):
            logging.info("cc: " + email.cc)

        logging.info("date: " + email.date)

        html_bodies = email.bodies('text/html')

        for content_type, body in html_bodies:
            logging.info('content_type: ' + content_type)
            decoded_body = body.decode()
            logging.info('decoded_body: ' + decoded_body)

        plaintext_bodies = email.bodies('text/plain')

        for content_type, body in plaintext_bodies:
            logging.info('content_type: ' + content_type)
            decoded_body = body.decode()
            logging.info('decoded_body: ' + decoded_body)




