from source.framework.webapp2_helpers import make_routes
from source.api.Conversations import ConversationsApi
from source.api.Users import UsersApi

app = make_routes([
    ('/api/conversations/.*', ConversationsApi),
    ('/api/users/.*', UsersApi)
])
