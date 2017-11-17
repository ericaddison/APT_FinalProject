import logging
import source.framework.SendGrid as sg
try:
    import source.config.authentication as conf
except ImportError:
    import source.config.authentication_dummy as conf

# interface to send messages from the comm options: web, email, sms
# currently sends to ALL, including self


def broadcast_message(convmsg):
    """Send new message to all users of a conversation"""
    logging.debug("Sending message \"{}\" from {} to all".format(convmsg.get_text(), convmsg.alias))

    if conf.AUTH_PROVIDER == conf.auth_demo:
        return

    conv = convmsg.get_conversation()

    convusers = conv.get_active_convusers()

    for convuser in convusers:
        if convuser.commOption == 'web':
            send_to_web(convmsg, convuser.commDetail)
        elif convuser.commOption == 'email':
            send_to_email(convmsg, convuser.commDetail)
        elif convuser.commOption == 'sms':
            send_to_sms(convmsg, convuser.commDetail)
        else:
            logging.warning("Unknown comm option: {}".format(convuser.commOption))


def send_to_web(convmsg, comm_detail):
    logging.debug('sending web message to {}'.format(comm_detail))


def send_to_email(convmsg, comm_detail):
    logging.debug('sending email message to {}'.format(comm_detail))
    sg.send_email_from_convmsg(comm_detail,
                                    convmsg,
                                    '{}'.format(convmsg.get_conversation().name)
                               )


def send_to_sms(convmsg, comm_detail):
    logging.debug('sending sms message to {}'.format(comm_detail))