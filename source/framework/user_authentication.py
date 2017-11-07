import urllib2
from source.config.authentication import *


def user_authentication(auth_header):
    user = None

    parts = auth_header.split()
    if len(parts) != 2:
        print("user_authentication(): improper authorization header length");
        return None

    if parts[0].lower() != 'bearer':
        print("user_authentication(): not a bearer header");
        return None

    access_token = parts[1]

    if verify_token(access_token):
        user = get_user_from_token(access_token)
    return user


def get_user_from_token(access_token):
    if AUTH_PROVIDER == auth_auth0:
        return get_user_from_token_auth0(access_token)


def verify_token(access_token):
    print("Attempting to verify {0} access_token {1}".format(AUTH_PROVIDER, access_token))
    if AUTH_PROVIDER == auth_auth0:
        return verify_token_auth0(access_token)


# verify token and return boolean success
def verify_token_auth0(access_token):
    print("verify_token(): Failed to verify auth0 token {}".format(access_token));
    return False


# last step maybe? After verifying token?
def get_user_from_token_auth0(access_token):
    base_url = "https://{domain}".format(domain=AUTH0_DOMAIN)
    userinfo = base_url + "/userinfo?access_token=" + access_token
    response = urllib2.urlopen(userinfo)
    data = response.read()
    #return get_user_from_email(data.email)
    print("get_user_from_token(): Failed to find user");
    return None