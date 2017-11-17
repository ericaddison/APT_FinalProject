import sendgrid
from source.config.authentication import SENDGRID_API_KEY, EMAIL_DOMAIN
from sendgrid.helpers.mail import *
import logging


def send_email(to, sender, subject, text):
    try:
        logging.debug('sending SendGrid email to {}'.format(to))
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email("{}@{}".format(sender, EMAIL_DOMAIN))
        to_email = Email(to)
        content = Content("text/html", text)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        logging.debug(response.status_code)
        logging.debug(response.body)
        logging.debug(response.headers)
    except Exception, e:
        logging.warning("Exception in SendGrid::send_email!!!")
        logging.warning(e.message)


def send_email_from_convuser(to, cuser, subject, text):
    conv = cuser.get_conversation()
    send_email(to, '{}_{}'.format(cuser.displayName, conv.get_id()), subject, text)


def send_email_from_convmsg(to, convmsg, subject):
    send_email(to, '{}_{}'.format(convmsg.alias, convmsg.get_conversation_id()), subject, convmsg.get_text())
