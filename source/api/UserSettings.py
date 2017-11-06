from source.framework.ApiServiceHandler import ApiServiceHandler


def get_user_settings(email=""):
    """Get user settings by email"""
    response = {}
    response['user-settings'] = "User settings"
    return response


def update_user_settings(email):
    """Update user settings"""
    response = {}
    response['user-settings'] = "Updated user settings"
    return response


class UserSettingsApi(ApiServiceHandler):
    """REST API handler to allow interaction with user settings"""

    def get_hook(self):
        """Get user settings for a user"""
        return get_user_settings()

    def put_hook(self):
        """Update user settings for a user"""
        response = update_user_settings()