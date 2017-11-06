from source.framework.ApiServiceHandler import ApiServiceHandler


def get_users(email=""):
    """Get user settings by email"""
    response = {}
    response['user-settings'] = "User settings"
    return response


def update_user(email):
    """Update user settings"""
    response = {}
    response['user-settings'] = "Updated user settings"
    return response


class UsersApi(ApiServiceHandler):
    """REST API handler to allow interaction with user settings"""

    def get_hook(self):
        """Get user settings for a user"""
        return get_users()

    def put_hook(self):
        """Update user settings for a user"""
        return update_user()