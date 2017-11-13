from google.appengine.ext import ndb


class ConvMessages(ndb.Model):
    user = ndb.KeyProperty(indexed=True, kind='Users')
    alias = ndb.StringProperty(indexed=True)
    conv = ndb.KeyProperty(indexed=True, kind='Conversations')
    postDate = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
    text = ndb.StringProperty()
    mediaURL = ndb.StringProperty()
    deleted = ndb.BooleanProperty()

    def get_id(self):
        return long(self.key.id())

    def get_basic_data(self):
        return {'id': self.get_id(),
                'userAlias': self.alias,
                'postDate': str(self.postDate)}

    def is_owner(self, user):
        """Check if the given user is the owner"""
        return user.key == self.user

    def get_full_data(self):
        """Get full data for this message ... everything except userid"""
        data = self.get_basic_data()
        data['convID'] = self.conv.id()
        data['text'] = self.text
        data['mediaURL'] = self.mediaURL
        data['deleted'] = self.deleted
        data['convName'] = self.conv.get().name
        return data

    def delete(self):
        self.deleted = True
        self.put()
        return self

    @classmethod
    def create(cls, user, user_alias, conv, text, media_url):
        msg = ConvMessages(user=user.key,
                           alias=user_alias,
                           conv=conv.key,
                           text=text,
                           mediaURL=media_url,
                           deleted=False)
        msg.put()
        return msg

    @classmethod
    def get_messages_by_user(cls, user_id):
        return ConvMessages.query(ConvMessages.user == user_id)

    @classmethod
    def get_by_id(cls, msg_id):
        return ndb.Key('ConvMessages', long(msg_id)).get()

    @classmethod
    def get_recent_conversation_messages(cls, convID, sinceDateTime):
        return #messages since dateTime
