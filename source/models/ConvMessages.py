from google.appengine.ext import ndb
from datetime import datetime

class ConvMessages(ndb.Model):
    user = ndb.KeyProperty(indexed=True, kind='Users')
    alias = ndb.StringProperty(indexed=True)
    conv = ndb.KeyProperty(indexed=True, kind='Conversations')
    postDate = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
    edits = ndb.JsonProperty(repeated=True)
    deleted = ndb.BooleanProperty()

    def get_id(self):
        return long(self.key.id())

    def get_text(self):
        return self.edits[-1]['text']

    def get_media_url(self):
        return self.edits[-1]['mediaURL']

    def get_basic_data(self):
        return {'id': self.get_id(),
                'userAlias': self.alias,
                'postDate': str(self.postDate)}

    def get_conversation(self):
        return self.conv.get()

    def check_owner(self, user):
        """Check if the given user is the owner"""
        return user.key == self.user

    def check_conv(self, conv):
        """Check if the given conv matches"""
        return conv.key == self.conv

    def get_full_data(self):
        """Get full data for this message ... everything except userid"""
        data = self.get_basic_data()
        data['convID'] = self.conv.id()
        data['text'] = self.edits[-1]['text']
        data['mediaURL'] = self.edits[-1]['media_url']
        data['editedDate'] = self.edits[-1]['date']
        data['deleted'] = self.deleted
        data['convName'] = self.conv.get().name
        data['edits'] = self.edits
        data['id'] = self.get_id()
        return data

    def delete(self):
        self.deleted = True
        self.put()
        return self

    def update(self, text=None, media_url=None):
        # update this to work with text and media url in edits instead of raw fields
        new_text = text if text else self.edits[-1]['text']
        new_media = media_url if media_url else self.edits[-1]['media_url']
        self.edits.append({'text': new_text, 'media_url': new_media, 'date': str(datetime.now())})
        self.put()

    @classmethod
    def create(cls, user, user_alias, conv, text, media_url):
        msg = ConvMessages(user=user.key,
                           alias=user_alias,
                           conv=conv.key,
                           deleted=False)
        msg.edits.append({'text': text, 'media_url': media_url, 'date': str(datetime.now())})
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
