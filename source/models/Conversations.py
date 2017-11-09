from google.appengine.ext import ndb

class Conversations(ndb.Model):
    owner = ndb.KeyProperty(indexed=True, kind='Users')
    name = ndb.StringProperty()
    password = ndb.StringProperty() #bcrypt hash value
    createDate = ndb.DateTimeProperty()
    destroyDate = ndb.DateTimeProperty()
    users = ndb.KeyProperty(repeated=True, kind='Users')
    idPolicy = ndb.StringProperty() #???
    viewAfterExpire = ndb.BooleanProperty()
    revealOwner = ndb.BooleanProperty()
    restrictComms = ndb.StringProperty() #???

    def get_all_conversations(self):
        return #list of all conversations

    def get_all_active_conversations(self):
        return #list of non-destroyed conversations

    def get_conversation_by_id(self, convID):
        return #conv details by conv ID

    def get_conversation_by_owner(self, ownerID):
        return #conv details by owner's user ID

    def get_conversation_users(self, convID):
        return #list of users in a specific conversation

    def check_conversation_password(self, convID, passwordHash):
        #use bcrypt to check pw hash param against stored
        #conversation password value
        return #boolean