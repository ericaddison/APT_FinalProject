from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from source.api.ConvMessages import create_message
from source.models.Users import Users
from source.models.ConvMessages import ConvMessages
import source.framework.communicate as comm
import logging
import re

# Incoming email assumptions:
#   - subject should be the conversation name ... but this is not necessary
#   - TO address should be conversation_<conv_id>@hailing-frequencies-2017.appspotmail.com


class GeneralMailHandler(InboundMailHandler):
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


class ConversationMailHandler(InboundMailHandler):
    """Web handler to incoming emails"""

    def __init__(self, arg1, arg2):
        super(InboundMailHandler, self).__init__(arg1, arg2)
        self.convid_regex = re.compile('conversation_(\d+)@.*')
        self.email_regex = re.compile('.*<(.*)>')

    def receive(self, email):
        logging.info("CONV: Received a message from: " + email.sender)
        logging.info("CONV: subject: " + email.subject)
        logging.info("CONV: to: " + email.to)

        # parse sender email
        match = self.email_regex.match(email.sender)
        sender = match.groups()[0]

        # parse conversation ID
        match = self.convid_regex.match(email.to)
        if not match:
            ConversationMailHandler.send_wtf_email(sender)
            self.response.set_status(404)
            return

        convID = match.groups()[0]
        logging.debug('found convid: {}'.format(convID))

        # make sure email is authorized
        user = Users.get_a_user(sender)
        if not user:
            logging.info('could not find user for email {}'.format(sender))
            # send error email
            self.response.set_status(404)
            return

        logging.debug('found user: {}'.format(user.get_id()))


        # put message in conversation
        message = []

        plaintext_bodies = email.bodies('text/plain')

        for content_type, body in plaintext_bodies:
            logging.info('content_type: ' + content_type)
            decoded_body = body.decode()
            logging.info('decoded_body: ' + decoded_body)
            message.append(decoded_body)

        response = create_message(user, convID, " ".join(message), "")
        logging.debug(response)

        # broadcast to others
        convmsg = ConvMessages.get_by_id(response['messages']['id'])
        if convmsg:
            comm.broadcast_message(convmsg)

    @classmethod
    def send_wtf_email(cls, to_address):
        pass