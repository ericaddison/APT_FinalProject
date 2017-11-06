from source.framework.webapp2_helpers import make_routes
from source.api.get_conversations import GetConversations

app = make_routes([
    ('/api/conversations', GetConversations)
])
