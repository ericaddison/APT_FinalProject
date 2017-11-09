import urllib2
import json
import lib.jwt as jwt
from lib.jwt.contrib.algorithms.pycrypto import RSAAlgorithm
from lib.jwt.contrib.algorithms.py_ecdsa import ECAlgorithm
from source.config.authentication import *


#jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
#jwt.register_algorithm('ES256', ECAlgorithm(ECAlgorithm.SHA256))

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
    print("get_user_from_token(): Failed to find user");
    return None