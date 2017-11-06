from source.framework.webapp2_helpers import make_routes
from source.api.Conversations import ConversationsApi
from source.api.UserSettings import UserSettingsApi

app = make_routes([
    ('/api/conversations', ConversationsApi),
    ('/api/usersettings', UserSettingsApi)
])
