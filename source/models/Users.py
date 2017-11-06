import ndb

class Users(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    fName = ndb.StringProperty
    lName = ndb.StringProperty
    joinDate = ndb.DateTimeProperty
    prefComm = ndb.StringProperty #Preferred Communication Method


    def get_users(self):
        return #list of all users

    def get_a_user(self, id):
        #if (id is integer, then it's the userID)
        #else (id is email)
        return #details on a specific user
