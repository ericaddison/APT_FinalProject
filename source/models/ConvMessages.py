from google.appengine.ext import ndb


class ConvMessages(ndb.Model):
    user = ndb.KeyProperty(indexed=True, kind='Users')
    alias = ndb.StringProperty(indexed=True)
    conv = ndb.KeyProperty(indexed=True, kind='Conversations')
    postDate = ndb.DateTimeProperty(indexed=True)
    text = ndb.StringProperty()
    mediaURL = ndb.StringProperty()

    def get_id(self):
        return long(self.key.id())

    def get_basic_data(self):
        return {'id': self.get_id(),
                'userAlias': self.alias,
                'postDate': self.postDate}

    def get_full_data(self):
        """Get full data for this message ... everything except userid"""
        data = self.get_basic_data()
        data['convID'] = self.conv.id()
        data['text'] = self.text
        data['mediaURL'] = self.mediaURL
        return data

    @classmethod
    def create(cls, user, user_alias, conv, text, media_url):
        msg = ConvMessages(user=user.key,
                           alias=user_alias,
                           conv=conv.key,
                           text=text,
                           mediaURL=media_url)
        msg.put()
        return msg

    @classmethod
    def get_messages_by_user(cls, user_id):
        return ConvMessages.query(ConvMessages.user == user_id)

    @classmethod
    def get_recent_conversation_messages(cls, convID, sinceDateTime):
        return #messages since dateTime
