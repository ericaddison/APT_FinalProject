from google.appengine.ext import ndb
from datetime import datetime
import random

class Conversations(ndb.Model):
    owner = ndb.KeyProperty(indexed=True, kind='Users')
    name = ndb.StringProperty()
    password = ndb.StringProperty() #bcrypt hash value
    createDate = ndb.DateTimeProperty(auto_now_add=True)
    destroyDate = ndb.DateTimeProperty(indexed=True)
    users = ndb.KeyProperty(repeated=True, kind='Users')
    aliases = ndb.StringProperty(repeated=True)
    idPolicy = ndb.StringProperty() #???
    viewAfterExpire = ndb.BooleanProperty()
    revealOwner = ndb.BooleanProperty()
    restrictComms = ndb.StringProperty() #???

    def get_conversation_users(self):
        return self.users

    def check_conversation_password(self, convID, passwordHash):
        #use bcrypt to check pw hash param against stored
        #conversation password value
        return False

    def get_id(self):
        return long(self.key.id())

    def get_basic_data(self):
        return {'id': self.get_id(),
                'name': self.name}

    def get_full_data(self):
        return {'id': self.get_id(),
                'name': self.name,
                'createDate': str(self.createDate),
                'destroyDate': str(self.destroyDate),
                'aliases': self.aliases,
                'idPolicy': self.idPolicy,
                'viewAfterExpire': self.viewAfterExpire,
                'revealOwner': self.revealOwner,
                'restrictComms': self.restrictComms}

    def has_user(self, user):
        return user.key in self.users or user.key == self.owner

    def get_messages(self):
        return "all the messages :)"

    @classmethod
    def get_all_conversations(cls):
        return Conversations.query().fetch()

    @classmethod
    def get_all_active_conversations_basic_data(cls):
        return [conv.get_basic_data() for conv in cls.get_all_active_conversations()]

    @classmethod
    def get_all_active_conversations(cls):
        return Conversations.query(Conversations.destroyDate > datetime.now())

    @classmethod
    def get_conversation_by_id(cls, convID):
        return ndb.Key('Conversations', long(convID)).get()

    @classmethod
    def get_conversation_by_owner(cls, ownerID):
        return ndb.query(Conversations.owner == ownerID)

    @classmethod
    def get_conversations_by_name(cls, name):
        query0 = Conversations.query()
        query1 = query0.filter(Conversations.name == name)
        query2 = query1.filter(Conversations.destroyDate > datetime.now())
        return query2.fetch()

    @classmethod
    def create(cls, owner, name, destroy_date, id_policy, view_after_expire, reveal_owner, restrict_comms, password_hash):

        if cls.get_conversations_by_name(name):
            return None

        conv = Conversations(owner=owner.key,
                             name=name,
                             destroyDate=destroy_date,
                             password=password_hash,
                             idPolicy=id_policy,
                             viewAfterExpire=view_after_expire,
                             revealOwner=reveal_owner,
                             restrictComms=restrict_comms)
        conv.put()
        return conv

    @classmethod
    def random_name(cls):
        good_name = False
        while not good_name:
            name = "conversation{}".format(random.randint(100000000000, 999999999999))
            good_name = (len(cls.get_conversations_by_name(name)) == 0)
        return name


id_policies = ["real_names", "user_alias", "colors", "numbers", "animals"]