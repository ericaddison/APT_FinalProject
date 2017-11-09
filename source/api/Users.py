from source.framework.ApiServiceHandler import ApiServiceHandler
import source.framework.constants as c
from source.models.Users import Users


def get_user(user):
    """Get user settings"""
    response = {}
    response['user-settings'] = user.get_user_data_dict()
    return response


def update_user():
    """Update user settings"""
    response = {}
    response['user-settings'] = "Updated user settings"
    return response


def create_user(email, fname, lname, prefcomm):
    """Create a user"""
    user = Users.create(email, fname, lname, prefcomm)
    return get_user(user)


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
        return get_user(user)

    def put_hook(self, user):
        """Update user settings for a user"""
        # update user settings by parsing incoming parameters and
        # updating database
        return update_user()

    def post_hook(self, user):
        """Create a new user"""

        # dummy version, for now
        fname = self.get_request_param(c.fname_parm)
        lname = self.get_request_param(c.lname_parm)
        email = self.get_request_param(c.email_parm)
        prefcomm = self.get_request_param(c.prefcomm_parm)

        print("handler: {}".format(self.get_request_parameter_dictionary()))

        # real version should ....
        # retrieve user info from access token and store in database
        # store as an unverified user until email verification
        return create_user(email, fname, lname, prefcomm)

    def delete_hook(self, user):
        """Delete a user"""
        # delete user info from database by email in the token info
        return delete_user()