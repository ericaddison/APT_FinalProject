from google.appengine.ext import ndb
from datetime import datetime
from source.models.ConvUsers import ConvUsers
from source.models.id_policies import colors_policy
import logging
import random


class Conversations(ndb.Model):
    owner = ndb.KeyProperty(indexed=True, kind='Users')
    name = ndb.StringProperty()
    messages = ndb.KeyProperty(kind='ConvMessages', repeated=True)
    password = ndb.StringProperty() #bcrypt hash value
    createDate = ndb.DateTimeProperty(auto_now_add=True)
    destroyDate = ndb.DateTimeProperty(indexed=True)
    aliases = ndb.KeyProperty(kind='ConvUsers', repeated=True)
    idPolicy = ndb.StringProperty() #???
    viewAfterExpire = ndb.BooleanProperty()
    revealOwner = ndb.BooleanProperty()
    restrictComms = ndb.StringProperty() #???

    def get_aliases(self):
        aliases = ndb.get_multi(self.aliases)
        return [alias.displayName for alias in aliases]

    def get_active_aliases(self):
        aliases = ndb.get_multi(self.aliases)
        return [alias.displayName for alias in aliases if alias.active]

    def get_active_convusers(self):
        aliases = ndb.get_multi(self.aliases)
        return [convuser for convuser in aliases if convuser.active]

    def get_active_users(self):
        aliases = ndb.get_multi(self.aliases)
        return [alias.user for alias in aliases if alias.active]

    def get_all_users(self):
        aliases = ndb.get_multi(self.aliases)
        return [alias.user for alias in aliases]

    def check_conversation_password(self, convID, passwordHash):
        #use bcrypt to check pw hash param against stored
        #conversation password value
        return False

    def get_id(self):
        return long(self.key.id())

    def get_basic_data(self):
        return {'id': self.get_id(),
                'name': self.name,
                'destroyDate': str(self.destroyDate)}

    def get_full_data(self):
        return {'id': self.get_id(),
                'name': self.name,
                'createDate': str(self.createDate),
                'destroyDate': str(self.destroyDate),
                'aliases': self.get_aliases(),
                'idPolicy': self.idPolicy,
                'viewAfterExpire': self.viewAfterExpire,
                'revealOwner': self.revealOwner,
                'restrictComms': self.restrictComms}

    def has_active_user(self, user):
        users = self.get_active_users()
        return user.key in users or user.key == self.owner

    def get_messages_basic_data(self):
        msgs = ndb.get_multi(self.messages)
        return [msg.get_basic_data() for msg in msgs]

    def get_messages_full_data(self):
        msgs = ndb.get_multi(self.messages)
        return [msg.get_full_data() for msg in msgs if not msg.deleted]

    def put_message(self, msg):
        self.messages.append(msg.key)
        self.put()

    def get_alias_for_user(self, user):
        cuser = ConvUsers.get_by_user_and_conv(user, self)
        if not cuser:
            return None
        return cuser.displayName

    def add_user(self, user, comm_option, comm_detail):
        """Add a user to the conversation. Return displayName (alias)"""
        # check if user already in conversation
        users = self.get_active_users()
        if user.key in users:
            return self.get_alias_for_user(user)

        # check if ConvUser already exists for this conv/user
        # e.g, if was part of the conversation but previously left
        cuser = ConvUsers.get_by_user_and_conv(user, self)

        # if ConvUser does not exist, create
        if not cuser:
            cuser = ConvUsers.create(user, self, self.idPolicy, comm_option, comm_detail)
            self.aliases.append(cuser.key)
        else:
            cuser.set_active(True)
        self.put()
        return cuser.displayName

    def remove_user(self, user):
        """Remove a user from the conversation. Return displayName (alias)"""
        # check if user already in conversation
        users = self.get_active_users()

        print(users)
        print(user)

        if user.key not in users:
            return None

        # retrieve ConvUser for this user/conversation
        cuser = ConvUsers.get_by_user_and_conv(user, self)
        cuser.set_active(False)
        return cuser.displayName

    @classmethod
    def get_all_conversations(cls):
        return Conversations.query().fetch()

    @classmethod
    def get_all_active_conversations_basic_data(cls):
        return [conv.get_basic_data() for conv in cls.get_all_active_conversations()]

    @classmethod
    def get_all_active_conversations(cls):
        allconvs = Conversations.query()
        return [conv for conv in allconvs if conv.destroyDate > datetime.now()]

    @classmethod
    def get_conversation_by_id(cls, convID):
        return ndb.Key('Conversations', long(convID)).get()

    @classmethod
    def get_conversation_by_owner(cls, owner):
        return Conversations.query(Conversations.owner == owner.key).fetch()

    @classmethod
    def get_conversations_by_name(cls, name):
        query0 = Conversations.query()
        query1 = query0.filter(Conversations.name == name)
        return query1.fetch()

    @classmethod
    def create(cls, owner, name, destroy_date, id_policy, view_after_expire, reveal_owner, restrict_comms, password_hash, comm_option='', comm_detail=''):

        conv = cls.get_conversations_by_name(name)
        if conv:
            return False, conv[0]

        # hard-coded colors policy for now
        id_policy = colors_policy['name']

        conv = Conversations(owner=owner.key,
                             name=name,
                             destroyDate=destroy_date,
                             password=password_hash,
                             idPolicy=id_policy,
                             viewAfterExpire=view_after_expire,
                             revealOwner=reveal_owner,
                             restrictComms=restrict_comms)

        # set owner alias
        conv.put()
        conv.add_user(owner, comm_option, comm_detail)
        return True, conv

    @classmethod
    def random_name(cls):
        good_name = False
        while not good_name:
            name = "conversation{}".format(random.randint(100000000000, 999999999999))
            good_name = (len(cls.get_conversations_by_name(name)) == 0)
        return name


id_policies = ["real_names", "user_alias", "colors", "numbers", "animals"]