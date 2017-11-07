from source.framework.ApiServiceHandler import ApiServiceHandler
from source.models.Users import Users


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
        # return user settings for a user based on email from access token
        return get_user()

    def put_hook(self, user):
        """Update user settings for a user"""
        # update user settings by parsing incoming parameters and
        # updating database
        return update_user()

    def post_hook(self, user):
        """Create a new user"""
        # retrieve user info from access token and store in database
        # store as an unverified user until email verification
        return create_user()

    def delete_hook(self, user):
        """Delete a user"""
        # delete user info from database by email in the token info
        return delete_user()