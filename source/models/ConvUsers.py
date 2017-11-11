from google.appengine.ext import ndb
from source.models.id_policies import *


class ConvUsers(ndb.Model):
    convID = ndb.KeyProperty(indexed=True, kind='Conversations')
    userID = ndb.KeyProperty(indexed=True, kind='Users')
    displayName = ndb.StringProperty() #for anonymous names
    muted = ndb.BooleanProperty()

    def get_user_names_by_convid(self, convID):
        return #list of display names

    @classmethod
    def create(cls, user, conv, id_policy):
        cuser = ConvUsers(convID=conv.key,
                          userID=user.key,
                          muted=False)

        #if id_policy == colors_policy['name']:
        cuser.displayName = get_name(conv, colors_policy)
        cuser.put()
        return cuser