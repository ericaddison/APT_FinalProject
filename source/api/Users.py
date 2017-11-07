from source.framework.ApiServiceHandler import ApiServiceHandler


def get_user(email=""):
    """Get user settings by email"""
    response = {}
    response['user-settings'] = "User settings"
    return response


def update_user():
    """Update user settings"""
    response = {}
    response['user-settings'] = "Updated user settings"
    return response


def create_user():
    """Create a user"""
    response = {}
    response['user-settings'] = "Newly created user settings"
    return response


def delete_user():
    """Delete a user"""
    response = {}
    response['user-settings'] = "Deleted user settings"
    return response


class UsersApi(ApiServiceHandler):
    """REST API handler to allow interaction with user settings"""

    def get_hook(self, user):
        """Get user settings for a user"""
        return get_user()

    def put_hook(self, user):
        """Update user settings for a user"""
        return update_user()

    def post_hook(self, user):
        """Create a new user"""
        return create_user()

    def delete_hook(self, user):
        """Delete a user"""
        return delete_user()