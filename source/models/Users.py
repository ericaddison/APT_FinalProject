from google.appengine.ext import ndb

class Users(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    fName = ndb.StringProperty()
    lName = ndb.StringProperty()
    joinDate = ndb.DateTimeProperty(auto_now_add=True)
    prefComm = ndb.StringProperty() #Preferred Communication Method

    def get_user_data_dict(self):
        return {"email": self.email,
                "fName": self.fName,
                "lName": self.lName,
                "joinDate": str(self.joinDate),
                "prefComm": self.prefComm}

    @classmethod
    def create(cls, email, fname, lname, prefcomm=""):
        user = Users(email=email,
                     fName=fname,
                     lName=lname,
                     prefComm=prefcomm
                     )
        print("email={}".format(email))
        user.put()
        return user

    @classmethod
    def get_users(self):
        return #list of all users

    @classmethod
    def get_a_user(self, id):
        #if (id is integer, then it's the userID)
        #else (id is email)
        return #details on a specific user
