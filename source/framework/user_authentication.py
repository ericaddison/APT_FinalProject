import urllib2
import json
import lib.jwt as jwt
from lib.jwt.contrib.algorithms.pycrypto import RSAAlgorithm
from lib.jwt.contrib.algorithms.py_ecdsa import ECAlgorithm
from source.config.authentication import *
from source.models.Users import Users

#appengine_config.py includes these from the lib directory
import google.auth.transport.requests
import google.oauth2.id_token

#Apparently the current version of requests is wonky are requires the monkeypatch to
#authenticate the firebase tokens
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()


#jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
#jwt.register_algorithm('ES256', ECAlgorithm(ECAlgorithm.SHA256))

def user_authentication(auth_header):
    user = None

    parts = auth_header.split()
    if len(parts) != 2:
        print("user_authentication(): improper authorization header length")
        return None

    if parts[0].lower() != 'bearer':
        print("user_authentication(): not a bearer header")
        return None

    access_token = parts[1]

    if verify_token(access_token):
        print("***Firebase User Verified")
        user = get_user_from_token(access_token)
    return user


def get_user_from_token(access_token):
    if AUTH_PROVIDER == auth_auth0:
        return get_user_from_token_auth0(access_token)
    elif AUTH_PROVIDER == auth_demo:
        return get_user_from_token_debug(access_token)
    elif AUTH_PROVIDER == auth_firebase:
        return get_user_from_token_firebase(access_token)


def verify_token(access_token):
    print("Attempting to verify {0} access_token {1}".format(AUTH_PROVIDER, access_token))
    if AUTH_PROVIDER == auth_auth0:
        return verify_token_auth0(access_token)
    elif AUTH_PROVIDER == auth_demo:
        return verify_token_debug(access_token)
    elif AUTH_PROVIDER == auth_firebase:
        return verify_token_firebase(access_token)


def verify_token_debug(access_token):
    if access_token in ['DEVTOKEN1', 'DEVTOKEN2']:
        return True
    return False


# verify token and return boolean success
def verify_token_firebase(access_token):
    claims = google.oauth2.id_token.verify_firebase_token(access_token, google.auth.transport.requests.Request())
    if not claims:
        return False
    return True


# verify token and return boolean success
def verify_token_auth0(access_token):

    jsonurl = urllib2.urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(access_token)
    except jwt.JWTError:
        print("Invalid header: Use an RS256 signed JWT Access Token")

    if unverified_header["alg"] == "HS256":
        print("Invalid header: Use an RS256 signed JWT Access Token")

    print(unverified_header)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
               payload = jwt.decode(
                access_token,
                rsa_key,
                algorithms=["RS256"],
                audience=AUTH0_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/"
            )
        except Exception, e:
            print(e.message)
            print("Unable to parse authentication token.")

    print("success???");
    return False


# last step maybe? After verifying token?
def get_user_from_token_auth0(access_token):
    base_url = "https://{domain}".format(domain=AUTH0_DOMAIN)
    userinfo = base_url + "/userinfo?access_token=" + access_token
    response = urllib2.urlopen(userinfo)
    data = response.read()
    #return get_user_from_email(data.email)
    print("get_user_from_token(): Failed to find user")
    return None


def get_user_from_token_debug(access_token):
    if access_token == 'DEVTOKEN1':
        return Users.dummy_user(1)
    elif access_token == 'DEVTOKEN2':
        return Users.dummy_user(2)


def get_user_from_token_firebase(access_token):
    #TODO: Patrick fill in here
    #Added token field to Users, query Users with access_token to retreive user
    return None
