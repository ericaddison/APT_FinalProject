from google.appengine.ext import ndb
from source.models.ConvUsers import ConvUsers
from source.models.Conversations import Conversations


class Users(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    fName = ndb.StringProperty(indexed=False)
    lName = ndb.StringProperty(indexed=False)
    joinDate = ndb.DateTimeProperty(auto_now_add=True)
    prefComm = ndb.StringProperty(indexed=False) #Preferred Communication Method
    prefCommDetail = ndb.StringProperty(indexed=False) #Preferred Communication Detail (email, phone number, etc)
    premium = ndb.BooleanProperty(indexed=True)
    verified = ndb.BooleanProperty(indexed=True)

    def get_id(self):
        return long(self.key.id())

    def get_full_data(self):
        response= {'id': self.get_id(),
                'email': self.email,
                'fName': self.fName,
                'lName': self.lName,
                'joinDate': str(self.joinDate),
                'prefComm': self.prefComm,
                'premium': self.premium,
                'verified': self.verified}

        convs = {'owned': self.get_owned_conversations(), 'joined': self.get_owned_conversations()}
        response['conversations'] = convs

        return response

    def get_joined_conversations(self):
        query0 = ConvUsers.query()
        convs = query0.filter(ConvUsers.user == self.key).fetch()
        return [conv.get_basic_data() for conv in convs]

    def get_owned_conversations(self):
        convs = Conversations.get_conversation_by_owner(self)
        return [conv.get_basic_data() for conv in convs]

    def commit(self):
        self.put()

    def delete(self):
        self.key.delete()

    @classmethod
    def create(cls, email, fname, lname, verified=False, prefcomm='email', prefcomm_detail=''):
        if Users.get_a_user(email):
            return None

        if prefcomm == 'email' and not prefcomm_detail:
            prefcomm_detail = email

        user = Users(email=email,
                     fName=fname,
                     lName=lname,
                     prefComm=prefcomm,
                     prefCommDetail = prefcomm_detail,
                     premium=False,
                     verified=verified
                     )
        user.put()
        return user

    @classmethod
    def get_users(cls):
        return Users.query().fetch()

    @classmethod
    def get_a_user(cls, email=None, user_id=None):
        if email:
            user_query0 = Users.query()
            user_query1 = user_query0.filter(Users.email == email)
            return user_query1.get()
        elif user_id:
            try:
                return ndb.Key('Users', long(user_id)).get()
            except ValueError:
                pass
        return None

    @classmethod
    def dummy_user(cls, dummyid=1):
        """Get or create a dummy user for testing ... really should authenticate via token"""
        if dummyid == 1:
            user = Users.get_a_user(user_id=123456789)
            if not user:
                user = Users(email="test@example.com",
                             fName="Testy",
                             lName="Testerson",
                             id=123456789,
                             prefComm="email",
                             premium=True,
                             verified=True
                             )
                user.put()
            return user
        elif dummyid == 2:
            user = Users.get_a_user(user_id=987654321)
            if not user:
                user = Users(email="serious@example.com",
                             fName="Lemon",
                             lName="Zest",
                             id=987654321,
                             prefComm="sms",
                             premium=False,
                             verified=True)
                user.put()
            return user
        else:
            user = Users.get_a_user(user_id=111666)
            if not user:
                user = Users(email="unverified@dude.com",
                             fName="No",
                             lName="Way",
                             id=111666,
                             prefComm="sms",
                             premium=False,
                             verified=False)
                user.put()
            return user

