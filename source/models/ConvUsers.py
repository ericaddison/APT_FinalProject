import ndb

class ConvUsers(ndb.Model):
    convID = ndb.KeyProperty(indexed=True, kind='Conversations')
    userID = ndb.KeyProperty(indexed=True, kind='Users')
    displayName = ndb.StringProperty #for anonymous names
    muted = ndb.BooleanProperty

    def get_user_names_by_convid(self, convID):
        return #list of display names
