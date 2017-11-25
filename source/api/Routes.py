from source.framework.webapp2_helpers import make_routes
from source.api.Conversations import ConversationsApi
from source.api.Conversations import OwnedConversationsApi
from source.api.ConvMessages import ConvMessagesApi
from source.api.ConvUsers import ConvUsersApi
from source.api.Users import UsersApi
from source.api.api_test import ApiTestCallback, ApiTestAuth

app = make_routes([
    ('/api/callback', ApiTestCallback),
    ('/api/test', ApiTestAuth),
    ('/api/conversations/(\d*)/messages/(\d*)', ConvMessagesApi),
    ('/api/conversations/(\d*)/users/(\d*)', ConvUsersApi),
    ('/api/conversations/(\d*)', ConversationsApi),
    ('/api/ownedconversations/', OwnedConversationsApi),
    ('/api/users/', UsersApi)
])
