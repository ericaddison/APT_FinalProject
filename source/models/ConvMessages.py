from google.appengine.ext import ndb

class ConvMessages(ndb.Model):
    userID = ndb.KeyProperty(indexed=True, kind='Users')
    convID = ndb.KeyProperty(indexed=True, kind='Conversations')
    postDate = ndb.DateTimeProperty()
    message = ndb.StringProperty()

    def get_messages_by_conversation(self, convID):
        return #messages

    def get_messages_by_user(self, userID):
        return #messages

    def get_recent_conversation_messages(self, convID, sinceDateTime):
        return #messages since dateTime
