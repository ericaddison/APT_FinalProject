import sendgrid
from source.config.authentication import SENDGRID_API_KEY, EMAIL_DOMAIN
from sendgrid.helpers.mail import *
import logging


def send_email(to, sender, subject, text):
    logging.debug('sending SendGrid email to {}'.format(comm_detail))
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email("{}@{}".format(sender, EMAIL_DOMAIN))
    to_email = Email(to)
    content = Content("text/plain", text)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    logging.debug(response.status_code)
    logging.debug(response.body)
    logging.debug(response.headers)


def send_email_from_conversation(to, conv, subject, text):
    send_email(to, 'conversation_{}'.format(conv.get_id()), subject, text)