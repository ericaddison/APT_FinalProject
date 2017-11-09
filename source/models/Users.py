from google.appengine.ext import ndb


class Users(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    fName = ndb.StringProperty(indexed=False)
    lName = ndb.StringProperty(indexed=False)
    joinDate = ndb.DateTimeProperty(auto_now_add=True)
    prefComm = ndb.StringProperty(indexed=False) #Preferred Communication Method

    def get_id(self):
        return long(self.key.id())

    def get_user_data_dict(self):
        return {"id": self.get_id(),
                "email": self.email,
                "fName": self.fName,
                "lName": self.lName,
                "joinDate": str(self.joinDate),
                "prefComm": self.prefComm}

    def commit(self):
        self.put()

    def delete(self):
        self.key.delete()

    @classmethod
    def create(cls, email, fname, lname, prefcomm=""):
        if Users.get_a_user(email):
            return None

        user = Users(email=email,
                     fName=fname,
                     lName=lname,
                     prefComm=prefcomm
                     )
        print("email={}".format(email))
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
            return user_query1.fetch()
        elif user_id:
            try:
                return ndb.Key('Users', long(user_id)).get()
            except ValueError:
                pass
        return None
