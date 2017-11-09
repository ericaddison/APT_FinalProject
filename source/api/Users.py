from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE
import source.framework.constants as c
from source.models.Users import Users

WRONG_USER_RESPONSE = {'message': 'Attempted to access non-self user', 'status': 403}


# [BEGIN API python methods]

def get_user(user, user_id):
    """Get user settings"""
    if user.get_id() != user_id:
        return WRONG_USER_RESPONSE
    return {'user-settings': user.get_user_data_dict()}


def update_user(user, user_id, fname="", lname="", prefcomm=""):
    """Update user settings"""
    if user.get_id() != user_id:
        return WRONG_USER_RESPONSE

    if fname:
        user.fName = fname
    if lname:
        user.lName = lname
    if prefcomm:
        user.prefComm = prefcomm
    user.commit()
    return {'user-settings': user.get_user_data_dict()}


def create_user(email, fname, lname, prefcomm):
    """Create a user"""
    user = Users.create(email, fname, lname, prefcomm)
    if user:
        return get_user(user)
    return {'message': 'Email already in use', 'status': 403}


def delete_user(user, user_id):
    """Delete a user"""
    if user.get_id() != user_id:
        return WRONG_USER_RESPONSE
    user.delete()
    return {'message': 'Deleted user {}'.format(user_id)}

# [END API python methods]


# [BEGIN API handler]

class UsersApi(ApiServiceHandler):
    """REST API handler to allow interaction with user settings"""

    def get_hook(self, user, url_id):
        """Get user settings for a user"""
        # return user settings for a user based on email from access token
        return get_user(user, url_id)

    def put_hook(self, user, url_id):
        """Update user settings for a user"""
        fname = self.get_request_param(c.fname_parm)
        lname = self.get_request_param(c.lname_parm)
        prefcomm = self.get_request_param(c.prefcomm_parm)
        return update_user(user, url_id, fname, lname, prefcomm)

    def post_hook(self, user, url_id):
        """Create a new user"""
        if url_id != 0:
            return NOT_FOUND_RESPONSE

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

    def delete_hook(self, user, url_id):
        """Delete a user"""
        # delete user info from database by email in the token info
        return delete_user(user, url_id)

# [END API handler]