# interface to receive and send messages from the comm options: web, email, sms

def broadcast_message(convmsg):
    """Send new message to all users of a conversation"""
    print("Sending message \"{}\" from {} to all".format(convmsg.get_text(), convmsg.alias))

    # for all web API users in conversation, send update (just update firebase???)

    # for all email users, send new email

    # for all SMS users, send text

