import logging
from google.appengine.ext import ndb
from source.models.id_policies import *
import source.framework.SendGrid as sg


# commOption is in ['web', 'email', 'sms']
# commDetail should be a properly formatted email for email, or phone number for sms, or ??? for web (firebase)

class ConvUsers(ndb.Model):
    conv = ndb.KeyProperty(indexed=True, kind='Conversations')
    user = ndb.KeyProperty(indexed=True, kind='Users')
    displayName = ndb.StringProperty() #for anonymous names
    muted = ndb.BooleanProperty()
    active = ndb.BooleanProperty(indexed=True)
    commOption = ndb.StringProperty()
    commDetail = ndb.StringProperty()

    def get_id(self):
        return long(self.key.id())

    def set_active(self, active):
        logging.debug("Setting cuser {} active".format(self.get_id()))
        self.active = active
        self.send_welcome_message()
        self.put()

    @classmethod
    def create(cls, user, conv, id_policy, comm_option, comm_detail):

        if not comm_option:
            comm_option = user.prefComm
            comm_detail = user.prefCommDetail

        cuser = ConvUsers(conv=conv.key,
                          user=user.key,
                          muted=False,
                          active=True,
                          commOption=comm_option,
                          commDetail=comm_detail)

        #if id_policy == colors_policy['name']:
        cuser.displayName = get_name(conv, colors_policy)
        cuser.put()
        return cuser

    def send_welcome_message(self):
        logging.debug("Sending welcome message to {}".format(self.get_id()))
        conv = self.conv.get()
        if self.commOption == 'email':

            email_text = """
            Hello!

            Welcome to the conversation \"{}\" on Hailing-Frequencies! We hope you'll have a great time.

            To interact with this conversation via email, just respond to this email message, or any other email you 
            receive regarding this conversation.
            
            Your alias for this conversation will be {}. As always, your true name and email address will not be revealed
            to the other users in the conversation.
            
            Happy hailing!
            
            -The HF Team  
            """.format(conv.name, self.alias)

            sg.send_email_from_conversation(self.commDetail,
                                            conv.get_id(),
                                            "Welcome to {}!".format(conv.name),
                                            email_text
                                            )

    @classmethod
    def get_by_user_and_conv(cls, user, conv):
        cuser = ConvUsers.query()
        cuser = cuser.filter(ConvUsers.conv == conv.key)
        cuser = cuser.filter(ConvUsers.user == user.key)
        return cuser.get()
