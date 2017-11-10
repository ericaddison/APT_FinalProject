from source.framework.webapp2_helpers import make_routes
from source.api.Conversations import ConversationsApi
from source.api.ConversationMessages import ConversationMessagesApi
from source.api.Users import UsersApi
from source.api.api_test import ApiTestCallback, ApiTestAuth

app = make_routes([
    ('/api/callback', ApiTestCallback),
    ('/api/test', ApiTestAuth),
    ('/api/conversations/(\d*)/messages/(\d*)', ConversationMessagesApi),
    ('/api/conversations/(\d*)', ConversationsApi),
    ('/api/users/(\d+)', UsersApi)
])
