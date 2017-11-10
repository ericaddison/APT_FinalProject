from google.appengine.ext import ndb


class ConvMessages(ndb.Model):
    userID = ndb.KeyProperty(indexed=True, kind='Users')
    userAlias = ndb.StringProperty(indexed=True)
    convID = ndb.KeyProperty(indexed=True, kind='Conversations')
    postDate = ndb.DateTimeProperty(indexed=True)
    text = ndb.StringProperty()
    mediaURL = ndb.StringProperty()

    def get_id(self):
        return long(self.key.id())

    def get_basic_data(self):
        return {'id': self.get_id(),
                'userAlias': self.userAlias,
                'postDate': self.postDate}

    def get_full_data(self):
        """Get full data for this message ... everything except userid"""
        data = self.get_basic_data()
        data['convID'] = self.convID.id()
        data['text'] = self.text
        data['mediaURL'] = self.mediaURL
        return data

    @classmethod
    def create(cls, user, user_alias, conv, text, media_url):
        msg = ConvMessages(userID=user.key,
                           userAlias=user_alias,
                           convID=conv.key,
                           text=text,
                           mediaURL=media_url)
        msg.put()
        return msg

    @classmethod
    def get_messages_by_user(cls, user_id):
        return ConvMessages.query(ConvMessages.userID == user_id)

    @classmethod
    def get_recent_conversation_messages(cls, convID, sinceDateTime):
        return #messages since dateTime
