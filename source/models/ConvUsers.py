from google.appengine.ext import ndb
from source.models.id_policies import *


class ConvUsers(ndb.Model):
    conv = ndb.KeyProperty(indexed=True, kind='Conversations')
    user = ndb.KeyProperty(indexed=True, kind='Users')
    displayName = ndb.StringProperty() #for anonymous names
    muted = ndb.BooleanProperty()
    active = ndb.BooleanProperty(indexed=True)

    def get_user_names_by_convid(self, convID):
        return #list of display names

    def set_active(self, active):
        self.active = active
        self.put()

    @classmethod
    def create(cls, user, conv, id_policy):
        cuser = ConvUsers(conv=conv.key,
                          user=user.key,
                          muted=False,
                          active=True)

        #if id_policy == colors_policy['name']:
        cuser.displayName = get_name(conv, colors_policy)
        cuser.put()
        return cuser

    @classmethod
    def get_by_user_and_conv(cls, user, conv):
        cuser = ConvUsers.query()
        cuser = cuser.filter(ConvUsers.conv == conv.key)
        cuser = cuser.filter(ConvUsers.user == user.key)
        return cuser.get()
