from source.framework.ApiServiceHandler import ApiServiceHandler, NOT_FOUND_RESPONSE
import source.framework.constants as c
from source.models.Users import Users

WRONG_USER_RESPONSE = {'message': 'Attempted to access non-self user', 'status': 401}


# [BEGIN API python methods]

def get_user(user):
    """Get user settings"""
    return {'user': user.get_full_data(), 'status': 200}


def update_user(user, fname="", lname="", prefcomm=""):
    """Update user settings"""
    if fname:
        user.fName = fname
    if lname:
        user.lName = lname
    if prefcomm:
        user.prefComm = prefcomm
    user.commit()
    return {'user': user.get_full_data(), 'status': 200}


def delete_user(user):
    """Delete a user"""
    response = {'message': 'Deleted user {}'.format(user.get_id()), 'status': 200}
    user.delete()
    return response

# [END API python methods]


# [BEGIN API handler]

class UsersApi(ApiServiceHandler):
    """REST API handler to allow interaction with user settings"""

    def get_hook(self, user, *args, **kwargs):
        #user is a local user object
        """Get user settings for a user"""
        # return user settings for a user based on email from access token
        return get_user(user)

    def put_hook(self, user, *args, **kwargs):
        """Update user settings for a user"""
        print "put_hook:  ", args;
        fname = self.get_request_param(c.fname_parm)
        lname = self.get_request_param(c.lname_parm)
        prefcomm = self.get_request_param(c.prefcomm_parm)
        return update_user(user, fname, lname, prefcomm)

    def delete_hook(self, user, *args, **kwargs):
        """Delete a user"""
        # delete user info from database by email in the token info
        return delete_user(user)

# [END API handler]
