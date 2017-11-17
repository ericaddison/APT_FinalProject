import urllib2
import json
import logging
import lib.jwt as jwt
from source.models.Users import Users

#appengine_config.py includes these from the lib directory
import google.auth.transport.requests
import google.oauth2.id_token

#Apparently the current version of requests is wonky and requires the monkeypatch to
#authenticate the firebase tokens
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

# check if real authentication config file exists, otherwise use dummy
try:
    import source.config.authentication as conf
except ImportError:
    import source.config.authentication_dummy as conf


def user_authentication(auth_header):
    user = None

    parts = auth_header.split()
    if len(parts) != 2:
        logging.warning("user_authentication(): improper authorization header length")
        return None

    if parts[0].lower() != 'bearer':
        logging.warning("user_authentication(): not a bearer header")
        return None

    access_token = parts[1]

    if verify_token(access_token):
        user = get_user_from_token(access_token)
    return user


def get_user_from_token(access_token):
    if conf.AUTH_PROVIDER == conf.auth_auth0:
        return get_user_from_token_auth0(access_token)
    elif conf.AUTH_PROVIDER == conf.auth_demo:
        return get_user_from_token_debug(access_token)
    elif conf.AUTH_PROVIDER == conf.auth_firebase:
        return get_user_from_token_firebase(access_token)


def verify_token(access_token):
    logging.debug("Attempting to verify {0} access_token {1}".format(conf.AUTH_PROVIDER, access_token))
    if conf.AUTH_PROVIDER == conf.auth_auth0:
        return verify_token_auth0(access_token)
    elif conf.AUTH_PROVIDER == conf.auth_demo:
        return verify_token_debug(access_token)
    elif conf.AUTH_PROVIDER == conf.auth_firebase:
        return verify_token_firebase(access_token)


def verify_token_debug(access_token):
    if access_token in ['DEVTOKEN1', 'DEVTOKEN2', 'DEVTOKEN3']:
        return True
    return False


# verify token and return boolean success
def verify_token_firebase(access_token):
    data = google.oauth2.id_token.verify_firebase_token(access_token, google.auth.transport.requests.Request())
    if data['aud'] == conf.FIREBASE_AUD and data['iss'] == conf.FIREBASE_ISS:
        logging.info("***Firebase User Verified")
        return True
    logging.info("***Firebase User NOT Verified")
    return False


# verify token and return boolean success
def verify_token_auth0(access_token):

    jsonurl = urllib2.urlopen("https://" + conf.AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(access_token)
    except jwt.JWTError:
        logging.warning("Invalid header: Use an RS256 signed JWT Access Token")

    if unverified_header["alg"] == "HS256":
        logging.warning("Invalid header: Use an RS256 signed JWT Access Token")

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
                audience=conf.AUTH0_AUDIENCE,
                issuer="https://" + conf.AUTH0_DOMAIN + "/"
            )
        except Exception, e:
            logging.warning(e.message)
            logging.warning("Unable to parse authentication token.")

    return False


# last step maybe? After verifying token?
def get_user_from_token_auth0(access_token):
    base_url = "https://{domain}".format(domain=conf.AUTH0_DOMAIN)
    userinfo = base_url + "/userinfo?access_token=" + access_token
    response = urllib2.urlopen(userinfo)
    data = response.read()
    #return get_user_from_email(data.email)
    logging.debug("get_user_from_token(): Failed to find user")
    return None


def get_user_from_token_debug(access_token):
    if access_token == 'DEVTOKEN1':
        return Users.dummy_user(1)
    elif access_token == 'DEVTOKEN2':
        return Users.dummy_user(2)
    elif access_token == 'DEVTOKEN3':
        return Users.dummy_user(3)


def get_user_from_token_firebase(access_token):
    userDict = google.oauth2.id_token.verify_firebase_token(access_token, google.auth.transport.requests.Request())
    emailAddy = userDict.get('email')
    logging.debug("***emailAddy: {}".format(emailAddy))
    userAcct = Users.get_a_user(emailAddy)
    logging.debug("***userAcct: {}".format(userAcct))
    if userAcct:
        return userAcct

    # create new user account
    else:
        names = userDict.get('name').split()
        verified = (userDict['firebase']['sign_in_provider'] != 'password')
        if len(names) > 1:
            user = Users.create(emailAddy, names[0], names[1], verified)
        else:
            user = Users.create(emailAddy, names[0], None, verified)
        return user
